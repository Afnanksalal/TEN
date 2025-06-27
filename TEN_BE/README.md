# Entrepreneurial Navigator Backend

This project sets up the backend for the Entrepreneurial Navigator, an AI-powered platform for entrepreneurs.

## Getting Started

1.  **Clone this repository** (or run the script that created this structure).
2.  **Navigate to the project directory:** `cd entrepreneurial_navigator_backend`
3.  **Start with Docker Compose (recommended):**
    Ensure you have Docker and Docker Compose installed.
    ```bash
    docker-compose up --build -d
    ```
    This will build the Docker image, start the FastAPI application, and a Redis server.
4.  **Access the API:**
    *   API Documentation (Swagger UI): `http://localhost:8000/docs`
    *   API Documentation (ReDoc): `http://localhost:8000/redoc`

## Project Structure Overview

```
.
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── routers/
│   │       │   ├── risk.py
│   │       │   ├── reputation.py
│   │       │   └── matching.py
│   │       └── __init__.py
│   ├── core/
│   │   ├── config.py
│   │   ├── dependencies.py
│   │   └── redis.py
│   ├── data/
│   │   ├── investor_profiles.json
│   │   └── risk_rules.json
│   ├── models/
│   │   └── schemas.py
│   ├── services/
│   │   ├── risk_analyzer.py
│   │   ├── reputation_scanner.py
│   │   ├── investor_matcher.py
│   │   └── pitch_feedback_generator.py
│   └── main.py
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Next Steps

*   Populate the Pydantic schemas in `app/models/schemas.py`.
*   Implement the core logic within the services in `app/services/`.
*   Define the API endpoints in `app/api/v1/routers/` and connect them to your services.
*   Configure environment variables in a `.env` file (based on `.env.example`).
