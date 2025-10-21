#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys

from sqlalchemy.util import md5_hex

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from db import Base, SessionLocal, engine
from models_db import User


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Insert default admin if not exists
    db = SessionLocal()
    if not db.query(User).filter_by(username="admin").first():
        db.add(User(username="admin", hashed_password=md5_hex("123456")))
        db.commit()
    db.close()

    yield

    # Teardown (optional)
    Base.metadata.drop_all(bind=engine)


def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption(
        "--run-integration",
        action="store_true",
        default=False,
        help="Run integration tests (requires actual API)",
    )


def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test (requires actual API)"
    )


def pytest_collection_modifyitems(config, items):
    """Skip integration tests by default"""
    if not config.getoption("--run-integration"):
        skip_integration = pytest.mark.skip(
            reason="need --run-integration option to run"
        )
        for item in items:
            if "integration" in item.keywords:
                item.add_marker(skip_integration)
