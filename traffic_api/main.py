#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import os
from contextlib import asynccontextmanager
from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session
from sqlalchemy.util import md5_hex
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from auth import authenticate_user, create_access_token, get_current_user
from db import Base, engine, get_db
from jobs import JobQueue, StatusEnum
from models import MultiTrafficRequest, Token
from models_db import TrafficLog, User
from step2_traffic_analysis import GoogleMapsTrafficAnalyzer

# logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# config
RATE = os.getenv("RATE_LIMIT", "10/minute")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
JWT_SECRET = os.getenv("JWT_SECRET", "secret")

# FastAPI app
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = next(get_db())
    admin_pw = os.getenv("ADMIN_PASSWORD", "password123").strip()
    if not db.query(User).filter_by(username="admin").first():
        db.add(User(username="admin", hashed_password=md5_hex(admin_pw)))
        db.commit()
    yield


app = FastAPI(title="Google Maps Traffic Analyzer API", lifespan=lifespan)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.add_exception_handler(
    RateLimitExceeded,
    lambda request, exc: JSONResponse(
        status_code=429, content={"detail": "Too many requests"}
    ),
)

# static directory
os.makedirs("static/images/traffic_screenshots", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")


# Worker function for a single location
@retry(
    wait=wait_exponential(multiplier=1, min=2, max=20),
    stop=stop_after_attempt(2),
    retry=retry_if_exception_type(Exception),
)
def run_single_location_blocking(
    lat,
    lng,
    storefront_direction,
    day_of_week,
    target_time,
    proxy=None,
):
    analyzer = GoogleMapsTrafficAnalyzer(proxy=proxy)
    return analyzer.analyze_location_traffic(
        lat=lat,
        lng=lng,
        save_to_static=True,
        storefront_direction=storefront_direction,
        day_of_week=day_of_week,
        target_time=target_time,
    )


# JobQueue configuration
JOBQUEUE_MAX_JOBS = int(os.getenv("JOBQUEUE_MAX_JOBS", 2))  # concurrent jobs
JOBQUEUE_PER_JOB_CONCURRENCY = int(
    os.getenv("JOBQUEUE_PER_JOB_CONCURRENCY", 4)
)  # locations per job

job_queue = JobQueue(
    worker_callable=run_single_location_blocking,
    max_workers=JOBQUEUE_MAX_JOBS,
    per_job_concurrency=JOBQUEUE_PER_JOB_CONCURRENCY,
)


@app.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/analyze-batch")
@limiter.limit(RATE)
async def analyze_batch(
    request: Request, payload: MultiTrafficRequest, user=Depends(get_current_user)
):
    """
    Submit a batch (up to 20 locations). Returns job_id immediately.
    Client must poll /job/{job_id} to get status or results.
    """
    if not payload.locations:
        raise HTTPException(status_code=400, detail="No locations provided")
    if len(payload.locations) > 20:
        raise HTTPException(status_code=400, detail="Max 20 locations per request")

    job_payload = {
        "locations": [
            {
                "lat": loc.lat,
                "lng": loc.lng,
                "storefront_direction": loc.storefront_direction or "north",
                "day": loc.day,
                "time": loc.time,
            }
            for loc in payload.locations
        ],
        "proxy": payload.proxy,
        "request_base_url": str(request.base_url),
    }

    job_id = job_queue.submit(job_payload)
    return {"job_id": job_id, "status": StatusEnum.PENDING.value}


@app.post("/job/{job_id}/cancel")
async def cancel_job(job_id: str, user=Depends(get_current_user)):
    job = job_queue.cancel(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found!")

    return {
        "job_id": job_id,
        "status": (job["status"].value),
        "remaining": job.get("remaining"),
        "error": job.get("error"),
        "result": job.get("result"),  # partial results included
    }


@app.get("/job/{job_id}")
async def get_job(
    job_id: str, user=Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Return the job status if still running,
    or full result when job is completed.
    """

    job = job_queue.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found!")

    status = job.get("status")
    response = {"job_id": job_id, "status": status.value}

    if status in (StatusEnum.PENDING, StatusEnum.RUNNING):
        response["remaining"] = job.get("remaining")
        return response

    if status == StatusEnum.FAILED:
        job_queue.remove(job_id)
        response["error"] = job.get("error")
        return response

    # DONE: log results into DB if not already logged
    if status in (StatusEnum.DONE, StatusEnum.CANCELED) and job.get("result"):
        if not job.get("_logged_to_db"):
            try:
                results = job["result"].get("results", [])
                payload_locations = job["payload"].get("locations", [])
                for i, res in enumerate(results):
                    log = TrafficLog(
                        job_id=job_id,
                        lat=payload_locations[i].get("lat"),
                        lng=payload_locations[i].get("lng"),
                        score=res.get("score"),
                        method=res.get("method"),
                        screenshot_url=res.get("screenshot_url"),
                        details=res,
                        user_id=user.id,
                    )
                    db.add(log)
                db.commit()
                db.refresh(log)
                job["_logged_to_db"] = True
            except Exception as e:
                logger.warning(f"DB log failed for job {job_id}: {e}")

    job_queue.remove(job_id)

    response["remaining"] = job.get("remaining")
    response["result"] = job.get("result")
    response["error"] = job.get("error")
    return response
