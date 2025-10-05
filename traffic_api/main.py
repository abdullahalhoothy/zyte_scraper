#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
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
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from auth import authenticate_user, create_access_token, get_current_user
from config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    JOBQUEUE_MAX_JOBS,
    JOBQUEUE_PER_JOB_CONCURRENCY,
    RATE,
    logger,
)
from db import get_db
from jobs import JobQueue, JobStatusEnum
from models import MultiTrafficRequest, Token
from models_db import Job, TrafficLog
from step2_traffic_analysis import GoogleMapsTrafficAnalyzer
from utils import get_job_record, lifespan, update_job

# FastAPI app
limiter = Limiter(key_func=get_remote_address)

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


job_queue = JobQueue(
    worker_callable=run_single_location_blocking,
    max_workers=JOBQUEUE_MAX_JOBS,
    per_job_concurrency=JOBQUEUE_PER_JOB_CONCURRENCY,
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Log the error details
    logger.error(f"Global error: {str(exc)}")

    # Return a generic error response
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "Something went wrong. Please try again later.",
        },
    )


@app.post("/login", response_model=Token)
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


@app.post("/analyze-traffic")
@app.post("/analyze-batch")
@app.post("/analyze-locations")
@app.post("/analyze-points")
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
    status = JobStatusEnum.PENDING.value

    try:
        db = next(get_db())
        job = Job(uuid=job_id, status=status, user_id=user.id)
        db.add(job)
        db.commit()
    except Exception as e:
        logger.warning(f"DB log failed to create job {job_id}: {e}")

    return {"job_id": job_id, "status": status}


@app.get("/job/{job_id}")
async def get_job(
    job_id: str | None, user=Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Return the job status if still running,
    or full result when job is completed.
    """

    job = job_queue.get(job_id)
    if not job:
        result = get_job_record()
        if result:
            return result
        raise HTTPException(status_code=404, detail="Job not found")

    status = job.get("status")
    remaining = job.get("remaining", 0)
    response = {"job_id": job_id, "status": status.value}

    if status in (JobStatusEnum.PENDING, JobStatusEnum.RUNNING):
        response["remaining"] = remaining
        return response

    if status == JobStatusEnum.FAILED:
        job_queue.remove(job_id)
        error = job.get("error")
        response["error"] = error
        update_job(
            job_id, user.id, status=status.value, remaining=remaining, error=error
        )
        return response

    # DONE: log results into DB if not already logged
    if status in (JobStatusEnum.DONE, JobStatusEnum.CANCELED) and job.get("result"):
        if not job.get("_logged_to_db"):
            try:
                results = job["result"].get("results", [])
                payload_locations = job["payload"].get("locations", [])
                for i, res in enumerate(results):
                    log = TrafficLog(
                        lat=payload_locations[i].get("lat"),
                        lng=payload_locations[i].get("lng"),
                        score=res.get("score"),
                        method=res.get("method"),
                        screenshot_url=res.get("screenshot_url"),
                        details=res,
                        job_id=job_id,
                    )
                    db.add(log)
                db.commit()
                db.refresh(log)
                job["_logged_to_db"] = True
            except Exception as e:
                logger.warning(f"DB log failed for job {job_id}: {e}")

    job_queue.remove(job_id)

    response["remaining"] = remaining
    response["result"] = job.get("result")
    response["error"] = job.get("error")

    update_job(
        job_id,
        user.id,
        status=status.value,
        remaining=remaining,
        error=job.get("error"),
    )

    return response


@app.post("/job/{job_id}/cancel")
async def cancel_job(job_id: str, user=Depends(get_current_user)):
    job = job_queue.cancel(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    status = job.get("status").value
    remaining = job.get("remaining", 0)
    error = job.get("error")

    update_job(job_id, user.id, status=status, remaining=remaining, error=error)

    return {
        "job_id": job_id,
        "status": status,
        "remaining": remaining,
        "result": job.get("result"),  # partial results included
        "error": error,
    }
