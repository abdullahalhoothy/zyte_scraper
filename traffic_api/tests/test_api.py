#!/usr/bin/python3
# -*- coding: utf-8 -*-

import asyncio

import pytest
from httpx import ASGITransport, AsyncClient
from main import app, job_queue

API_URL = "http://localhost:8000"
LOGIN_DATA = {"username": "admin", "password": "123456"}


@pytest.mark.asyncio
async def test_login_and_get_token(setup_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=API_URL) as client:
        resp = await client.post(
            "/token",
            data=LOGIN_DATA,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        assert resp.status_code == 200
        token = resp.json()["access_token"]
        assert token
        return token


@pytest.mark.asyncio
async def test_batch_submit_and_poll(mocker, setup_db):
    # Patch worker so it returns predictable result
    def fake_worker(lat, lng, *args, **kwargs):
        return {"score": lat + lng, "method": "mock"}

    job_queue.worker_callable = fake_worker

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=API_URL) as client:
        # login
        resp = await client.post(
            "/token",
            data=LOGIN_DATA,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        token = resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # submit batch
        locations = [{"lat": i, "lng": i} for i in range(5)]
        resp2 = await client.post(
            "/analyze-batch", json={"locations": locations}, headers=headers
        )
        assert resp2.status_code == 200
        job_id = resp2.json()["job_id"]

        # poll until done
        for _ in range(10):
            r = await client.get(f"/job/{job_id}", headers=headers)
            data = r.json()
            if data["status"] == "done":
                results = data["result"]["results"]
                # ensure order preserved
                for i, res in enumerate(results):
                    assert res["score"] == i + i
                break
            await asyncio.sleep(0.1)
        else:
            pytest.fail("Job did not complete in time")


@pytest.mark.asyncio
async def test_analyze_traffic_single(mocker):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=API_URL) as client:
        # login
        resp = await client.post(
            "/token",
            data=LOGIN_DATA,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        token = resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # call analyze-batch
        resp2 = await client.post(
            "/analyze-batch",
            json={"locations": [{"lat": 37.77, "lng": -122.41}]},
            headers=headers,
        )
        assert resp2.status_code == 200


@pytest.mark.asyncio
async def test_analyze_traffic_concurrent(mocker):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=API_URL) as client:
        # login
        resp = await client.post(
            "/token",
            data=LOGIN_DATA,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        token = resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # fire multiple requests concurrently
        tasks = [
            client.post(
                "/analyze-batch",
                json={"locations": [{"lat": i, "lng": i}]},
                headers=headers,
            )
            for i in range(5)
        ]
        responses = await asyncio.gather(*tasks)

        assert all(r.status_code == 200 for r in responses)
