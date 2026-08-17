# AI Interview Coach

[![Backend CI](https://github.com/MichaelGreatorex/AI-Interview-Coach/actions/workflows/backend-ci.yml/badge.svg)](https://github.com/MichaelGreatorex/AI-Interview-Coach/actions/workflows/backend-ci.yml)
[![Backend CD](https://img.shields.io/website?down_color=red&down_message=down&label=CD%20Production&up_color=brightgreen&up_message=live&url=http%3A%2F%2Faiic-prod-alb-925692489.eu-west-2.elb.amazonaws.com)](http://aiic-prod-alb-925692489.eu-west-2.elb.amazonaws.com)

AI Interview Coach is being developed into a full AI-powered interview preparation platform that takes a candidates CV and the JD for the job they are applying for and generates a personalised interview simulation based on both documents. 

```
Please note: this AI Layer is a feature that is under current development and not included in the latest v0.1.0 Release.
```

## Status

The repository now contains a working, test-covered interview workflow foundation and Terraform-based AWS infrastructure.

Current implementation includes:

- FastAPI backend with session lifecycle and response submission endpoints.
- Next.js frontend scaffold and local development runtime.
- PostgreSQL persistence via SQLAlchemy + Alembic migrations.
- Local document storage provider used during interview startup.
- Infrastructure as Code in Terraform for core AWS services.

Planned AI features are kept in the roadmap below and are not yet implemented.

## Current Backend API

Base path: `/api/v1`

- `GET /health`: health check.
- `POST /interviews`: starts an interview session from uploaded CV and job description files.
- `POST /sessions/{interview_session_id}/responses`: saves an answer and returns interview progression state (`interview_complete`, `next_question`).
- `DELETE /sessions/{interview_session_id}`: deletes a session and related stored data.

Interview questions are currently served by an internal static question set and deterministic interview engine logic.

## Infrastructure As Code (Terraform)

The `infra/` directory now contains active Terraform configuration for AWS provisioning.

Implemented resources include:

- VPC networking: VPC, public/private subnets, internet gateway, NAT gateway, and route tables.
- Security groups: ALB, frontend ECS service, backend ECS service, and RDS access controls.
- Compute: ECS cluster, backend and frontend task definitions, backend and frontend ECS services.
- Load balancing: ALB, listeners, routing rules, backend/frontend target groups.
- Data and persistence: PostgreSQL RDS instance and DB subnet group.
- Container registry: ECR repositories for backend and frontend images.
- Observability: CloudWatch log group for ECS services.
- IAM: task execution role plus Secrets Manager access policy for DB credentials.

## CI/CD

GitHub Actions workflow: `.github/workflows/backend-ci.yml`

- Pull requests run CI checks (compose build, migrations, backend tests).
- Pushes to `main` and `develop` run the same pipeline and act as the current delivery gate.

## Local Development

### Runtime Requirements

- Docker Desktop with Docker Compose

Optional host tooling:

- Python `3.14` (for direct local pytest/alembic workflows)
- Node.js `24.18.0` and npm `11.16.0` (for direct frontend workflows)

### Start Full Stack

From repository root:

```bash
docker compose up --build
```

Services:

- Postgres: `127.0.0.1:5432`
- Backend (FastAPI): `http://127.0.0.1:8000`
- Frontend (Next.js): `http://127.0.0.1:3000`

Stop stack:

```bash
docker compose down
```

Reset volumes:

```bash
docker compose down -v
```

### Convenience Scripts

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

### Run Backend Tests

```bash
cd backend
source .venv/bin/activate
python -m pytest -vv ../tests
```

### Alembic Migrations

Containerized:

```bash
docker compose run --rm backend alembic upgrade head
docker compose run --rm backend alembic current
```

Local environment:

```bash
cd backend
source .venv/bin/activate
export DATABASE_URL=postgresql://ai_interview:ai_interview_dev_password@127.0.0.1:5432/ai_interview_coach
alembic revision --autogenerate -m "describe your change"
alembic upgrade head
```

## Tech Stack

### Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS

### Backend

- Python
- FastAPI
- SQLAlchemy
- Alembic
- Pydantic
- pytest

### Infrastructure

- Terraform
- AWS ECS (Fargate)
- AWS ALB
- AWS ECR
- AWS RDS (PostgreSQL)
- AWS CloudWatch

## Repository Layout

```text
/frontend            Next.js UI
/backend             FastAPI application
/backend/alembic     Database migrations
/infra               Terraform AWS infrastructure
/tests               API, unit, repository, and integration tests
/docs                Project documentation
```

## Roadmap (Planned AI Interview Coach Features)

These are planned target capabilities and remain part of the project direction:

- CV parsing and job-description understanding with AI assistance.
- AI-generated, role-specific interview questions.
- AI-based answer scoring and structured feedback (for example, clarity, depth, relevance, STAR structure).
- Personalized coaching loops and progress tracking over time.
- Adaptive difficulty, multi-interviewer simulation, and voice-based interview flows.
