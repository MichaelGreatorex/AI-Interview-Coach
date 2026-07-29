# AI Interview Coach

An AI-powered interview preparation platform that generates personalized interview questions from a candidate's CV and job description, simulates mock interviews, and evaluates responses using structured AI-driven rubrics.

---

[![Backend CI](https://github.com/MichaelGreatorex/AI-Interview-Coach/actions/workflows/backend-ci.yml/badge.svg)](https://github.com/MichaelGreatorex/AI-Interview-Coach/actions/workflows/backend-ci.yml)

---

## Overview

This project simulates a real-world interview experience by:

- Parsing a user's CV (PDF upload)
- Analyzing a job description
- Generating tailored interview questions
- Running a chat-based mock interview
- Scoring and providing structured feedback on answers

The system is fully deployed on AWS with CI/CD automation.

---

## Architecture

### Frontend Architecture

- Next.js

### Backend API Architecture

- FastAPI (Dockerized)

### Compute Architecture

- AWS ECS (Fargate)

### AWS Service Architecture

- S3 (CV storage)
- RDS (PostgreSQL)
- CloudWatch (logging)

### AI Layer

- OpenAI API

---

## Core Features

### CV And JD Analysis

- Extracts structured data from CV
- Parses job descriptions into skill requirements
- Identifies skill gaps and alignment

### Interview Generation

- Generates technical questions
- Generates behavioral questions
- Generates CV-specific probing questions

### Mock Interview Engine

- Chat-based interview flow
- Stateful session management
- Real-time question/answer loop

### AI Evaluation System

Each answer is scored using:

- Clarity
- Technical depth
- Relevance
- Structure (for example, STAR method)

Outputs:

- Score (1 to 10)
- Strengths and weaknesses
- Ideal improved answer

---

## Deployment

The system is deployed on AWS using containerized infrastructure.

### Deployment Components

- ECS (Fargate): backend service runtime
- S3: CV file storage
- RDS (PostgreSQL): persistent session storage
- ALB: API routing
- CloudWatch: logging and monitoring

---

## CI/CD Pipeline

Automated deployment via GitHub Actions:

1. Code pushed to `main`
2. Backend is linted and tested
3. Docker image is built
4. Image pushed to AWS ECR
5. ECS service updated automatically

---

## Tech Stack

### Frontend Stack

- Next.js `16.2.9`
- React `19.2.4`
- React DOM `19.2.4`
- TypeScript `5`
- Tailwind CSS `4`
- ESLint `9`

### Backend Stack

- Python `3.14`
- FastAPI `0.138.2`
- Pydantic `2.13.4`
- Pydantic Settings `2.11.0`
- SQLAlchemy `2.0.51`
- Alembic `1.18.5`
- Uvicorn `0.32.1`
- python-multipart `0.0.30`
- pytest `9.1.1`
- pytest-asyncio `1.4.0`
- httpx2 `2.5.0`
- OpenAI API (client package not added yet)

### Infrastructure Stack

- AWS ECS (Fargate)
- AWS S3
- AWS RDS (PostgreSQL)
- AWS ECR
- GitHub Actions

---

## Clone, Setup, And Run

If you are cloning this repository and want to run it locally, use the following runtime and commands.

### Required Runtime

- Docker Desktop (with Docker Compose)

Optional (only for host-based testing workflows):

- Node.js `24.18.0` via `nvm` for the frontend
- npm `11.16.0`
- Python `3.14`

The repository pins Python in `.python-version`, Node in `.nvmrc`, and backend dependencies in `backend/requirements.txt` and `backend/requirements-dev.txt`.

### Environment Files

- Backend settings are loaded from `backend/.env`
- A starter template is available at `backend/.env.example`

### Full Container Stack (Frontend + Backend + Postgres)

Docker Compose is the canonical local startup path. From repository root, start all three services:

```bash
docker compose up --build
```

Optional: override the local Postgres password for containers:

```bash
export POSTGRES_PASSWORD="your-local-password"
docker compose up --build
```

This starts:

- Postgres on `127.0.0.1:5432`
- Backend pytests (run once at startup) and then FastAPI on `http://127.0.0.1:8000`
- Next.js frontend on `http://127.0.0.1:3000`

If tests fail, the backend container exits and `docker compose up` reports the failure in backend logs.

Default local connection string (also in `backend/.env.example`):

```text
postgresql://ai_interview:ai_interview_dev_password@127.0.0.1:5432/ai_interview_coach
```

Stop the stack:

```bash
docker compose down
```

Reset Postgres data volume:

```bash
docker compose down -v
```

### Optional Wrapper Scripts

The scripts below now proxy to Docker Compose for convenience.

All services:

```bash
./scripts/dev-stack.sh up
./scripts/dev-stack.sh status
./scripts/dev-stack.sh down
```

Postgres only:

```bash
./scripts/postgres.sh up
./scripts/postgres.sh status
./scripts/postgres.sh down
```

### Run Tests Manually

```bash
cd backend
source .venv/bin/activate
python -m pytest -vv ../tests
```

### Database Migrations (Alembic)

The backend uses Alembic for database schema migrations.

#### Prerequisites

- Docker Compose is running the Postgres service
- The backend container has access to the database URL from `backend/.env` or the container environment

### Generate migration (example command)

```bash
docker compose run --rm backend \
    alembic revision --autogenerate -m "initial schema"
```

#### Run migrations from the backend container

```bash
docker compose run --rm backend alembic upgrade head
docker compose run --rm backend alembic current
```

#### Run migrations from the local backend environment

```bash
cd backend
source .venv/bin/activate
export DATABASE_URL=postgresql://ai_interview:ai_interview_dev_password@127.0.0.1:5432/ai_interview_coach
alembic current
alembic revision --autogenerate -m "describe your change"
alembic upgrade head
```

#### Common migration commands

```bash
alembic history
alembic downgrade -1
```

The migration configuration lives in `backend/alembic.ini` and the migration scripts live in `backend/alembic/versions/`.

### Test Suite Coverage

The backend test suite currently validates configuration behavior, basic API health behavior, and API route wiring.

#### `tests/test_config.py`

- `test_settings_parse_comma_separated_allowed_origins`
  - Verifies comma-separated `allowed_origins` input is parsed into a clean list.
- `test_settings_convert_empty_strings_to_none`
  - Verifies empty and whitespace values for optional settings become `None`.

#### `tests/test_health.py`

- `test_health_check`
  - Verifies `GET /api/v1/health` returns HTTP 200 and `{"status": "ok"}`.

#### `tests/test_routes.py`

- `test_openapi_includes_expected_v1_routes`
  - Parameterized test that verifies each expected v1 route is present in `GET /openapi.json`.
  - Covered routes:
    - `/api/v1/health`
    - `/api/v1/cv/upload`
    - `/api/v1/jd/upload`
    - `/api/v1/interview/start`
    - `/api/v1/interview/answer`
    - `/api/v1/sessions/{session_id}`

#### `tests/conftest.py`

- Provides the shared FastAPI `TestClient` fixture used by API tests.

#### Current Coverage Boundaries

- The suite currently checks route registration and API shape, not full business logic.
- Placeholder route handlers are intentionally not exercised yet.
- As route implementations are added, add behavior tests alongside each endpoint.

### Validate Frontend

```bash
cd frontend
npm run lint
npm run build
```

### Current Repository State

- The frontend lives in `frontend` as a Next.js App Router app
- The backend lives in `backend` as a FastAPI app
- Local runtime is intended to be container-first via Docker Compose
- The frontend validates with `npm run lint` and `npm run build` on Node `24.18.0`
- The only fully implemented backend endpoint today is the health check

---

## Project Structure

```text
/frontend           -> Next.js UI
/backend           -> FastAPI server
/backend/app/models -> SQLAlchemy models
/backend/alembic   -> Alembic migration configuration and scripts
/infra             -> Docker + CI/CD configs
/prompts           -> LLM prompt templates
/tests             -> Unit + integration tests
/docs              -> Architecture decisions
```

---

## Key Engineering Highlights

- End-to-end AI pipeline (CV -> JD -> interview -> scoring)
- LLM-based structured evaluation system
- Production-style cloud deployment on AWS
- Automated CI/CD pipeline
- Stateful conversational interview system

---

## Future Improvements

- Voice-based interview mode
- Adaptive difficulty questioning
- Multi-interviewer simulation
- Personal performance tracking over time
