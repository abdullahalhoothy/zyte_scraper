# Traffic API

Dockerized FastAPI service that runs Google Maps traffic analysis using Selenium.

## Description

Added a new FastAPI endpoint to serve traffic data. The route accepts relevant parameters, validates inputs, and returns structured JSON with traffic details. Basic error handling is included to ensure robustness. This lays the groundwork for integrating real-time traffic info into the app and can be extended with caching or auth in future iterations. Manual and unit tests confirm expected behavior.

## Quick start (local + docker)

1. Copy repo, create `.env` if needed.
2. Run:
   ```bash
   docker-compose up --build
   ```