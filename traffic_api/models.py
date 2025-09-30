#!/usr/bin/python3
# -*- coding: utf-8 -*-

from typing import Any, Dict, Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TrafficRequest(BaseModel):
    lat: float
    lng: float
    storefront_direction: str = "north"
    day_of_week: Optional[str] = None
    target_time: Optional[str] = None
    save_to_static: bool = True


class TrafficResponse(BaseModel):
    score: float
    method: str
    screenshot_url: Optional[str] = None
    details: Dict[str, Any] = {}
