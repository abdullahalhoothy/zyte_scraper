#!/usr/bin/python3
# -*- coding: utf-8 -*-

import asyncio
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager
from datetime import timedelta
from urllib.parse import urljoin

from auth import authenticate_user_db, create_access_token, get_current_user
from db import Base, engine, get_db
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from models import Token, TrafficRequest
from models_db import TrafficLog, User
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session
from sqlalchemy.util import md5_hex
from step2_traffic_analysis import GoogleMapsTrafficAnalyzer
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

logger = logging.getLogger(__name__)
RATE = os.getenv("RATE_LIMIT", "10/minute")  # max 10 requests per minute per IP
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

limiter = Limiter(key_func=get_remote_address)
executor = ThreadPoolExecutor(max_workers=5)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = next(get_db())
    admin_pw = os.getenv("ADMIN_PASSWORD", "password123").strip()
    if not db.query(User).filter_by(username="admin").first():
        db.add(User(username="admin", hashed_password=md5_hex(admin_pw)))
        db.commit()
    yield


app = FastAPI(title="Google Maps Traffic Analyzer", lifespan=lifespan)

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.add_exception_handler(
    RateLimitExceeded,
    lambda request, exc: JSONResponse(
        status_code=429, content={"detail": "Too many requests"}
    ),
)

# static files mount (make sure directory exists)
os.makedirs("static/images/traffic_screenshots", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.post("/token", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user_db(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}


# blocking analysis runner with retry/backoff
@retry(
    wait=wait_exponential(multiplier=1, min=2, max=30),
    stop=stop_after_attempt(3),
    retry=retry_if_exception_type(Exception),
)
def run_analysis_blocking(
    lat,
    lng,
    save_to_static,
    storefront_direction,
    day_of_week,
    target_time,
    selenium_url=None,
    proxy=None,
):
    analyzer = GoogleMapsTrafficAnalyzer(
        cleanup_driver=True, selenium_url=selenium_url, proxy=proxy
    )
    return analyzer.analyze_location_traffic(
        lat=lat,
        lng=lng,
        save_to_static=save_to_static,
        storefront_direction=storefront_direction,
        day_of_week=day_of_week,
        target_time=target_time,
    )


@app.post("/analyze-traffic")
@limiter.limit(RATE)
async def analyze_traffic(
    request: Request,
    payload: TrafficRequest,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    selenium_url = os.getenv("SELENIUM_URL", "http://localhost:4444/wd/hub")
    proxy = os.getenv("SELENIUM_PROXY", None)

    loop = asyncio.get_running_loop()

    try:
        result = await loop.run_in_executor(
            executor,
            run_analysis_blocking,
            payload.lat,
            payload.lng,
            payload.save_to_static,
            payload.storefront_direction,
            payload.day_of_week,
            payload.target_time,
            selenium_url,
            proxy,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {e}")

    # Build screenshot_url if screenshot saved to static
    screenshot_url = None
    screenshot_path = result.get("screenshot_path") or result.get(
        "pinned_screenshot_path"
    )
    if screenshot_path and payload.save_to_static:
        try:
            # expect screenshot_path inside /app/static/...; make relative to static
            rel = os.path.relpath(screenshot_path, os.path.abspath("static"))
            screenshot_url = urljoin(
                str(request.base_url), f"static/{rel.replace(os.sep, '/')}"
            )
        except Exception:
            screenshot_url = None

    result["screenshot_url"] = screenshot_url

    # save to DB logs
    try:
        log = TrafficLog(
            lat=payload.lat,
            lng=payload.lng,
            score=result.get("score"),
            method=result.get("method"),
            screenshot_url=screenshot_url,
            details=result,
        )
        db.add(log)
        db.commit()
    except Exception as e:
        logger.warning(f"Could not save log to DB: {e}")

    return JSONResponse(result)
