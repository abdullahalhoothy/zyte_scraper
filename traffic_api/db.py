#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DB_FILE = os.getenv("SQLITE_DB_FILE", "traffic.db")
DB_URL = f"sqlite:///{DB_FILE}"

# Important for SQLite multithreaded usage with FastAPI
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
