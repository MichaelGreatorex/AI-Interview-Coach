# AI Interview Coach

[![Backend CI](https://github.com/MichaelGreatorex/AI-Interview-Coach/actions/workflows/backend-ci.yml/badge.svg)](https://github.com/MichaelGreatorex/AI-Interview-Coach/actions/workflows/backend-ci.yml)
[![Backend CD](https://img.shields.io/website?down_color=red&down_message=down&label=CD%20Production&up_color=brightgreen&up_message=live&url=http%3A%2F%2Faiic-prod-alb-925692489.eu-west-2.elb.amazonaws.com)](http://aiic-prod-alb-925692489.eu-west-2.elb.amazonaws.com)

AI Interview Coach is being developed into a full AI-powered interview preparation platform. The long-term target is personalized interview simulation using candidate CV and job description context.

Today, the repository ships a stable, test-covered interview workflow foundation with document upload, review, interview progression, and infrastructure automation.

## Current Implementation

- FastAPI backend with session lifecycle endpoints and response progression logic.
- Next.js frontend with multi-stage flow: upload, review extracted text, interview, complete.
- PostgreSQL persistence via SQLAlchemy and Alembic.
- Local file storage provider for uploaded documents.
- Terraform configuration for ECS, ALB, RDS, IAM, networking, and ECR.

## Current API

Base path: /api/v1

- GET /health
- POST /interviews
  - Accepts multipart CV and job description uploads.
  - Creates a new session and stores both documents.
- PATCH /interviews/{interview_session_id}/documents/{document_id}
  - Updates extracted document text before interview start.
- POST /interviews/{interview_session_id}/start
  - Starts interview and returns first question.
- POST /sessions/{interview_session_id}/responses
  - Saves response and returns interview state:
    - interview_complete
    - next_question
- DELETE /sessions/{interview_session_id}
  - Deletes session and associated document/response data.

Interview questions currently come from deterministic internal logic and seeded question data. AI-generated questioning remains part of the roadmap.

## Secure by Design

Security controls already applied in the current implementation:

1. Strict upload validation
- Why: Uploaded files are a high-risk input boundary.
- How: Files are prepared once, then validated for filename, size, and allowlisted MIME types before session creation.
- Effect: Malformed, empty, oversized, or unsupported uploads are rejected early.

2. Centralized file size enforcement
- Why: Security checks duplicated in many places tend to drift.
- How: Shared upload-size validation is used in both upload preparation and validator layers.
- Effect: One source of truth for max-size behavior and error handling.

3. Explicit CORS allowlist parsing
- Why: Overly broad origin handling can expose APIs to unauthorized browser contexts.
- How: allowed_origins supports controlled comma-separated and JSON-array configuration formats.
- Effect: CORS rules stay explicit and predictable across local and deployed environments.

4. Production fail-fast configuration
- Why: Missing secrets should fail at startup, not during runtime requests.
- How: Production settings require database configuration and OpenAI key.
- Effect: Misconfigured production deployments fail safely and quickly.

5. Network segmentation in AWS
- Why: Reduce attack surface and lateral movement opportunities.
- How: ECS services run in private subnets, RDS is not publicly accessible, and security groups restrict access paths.
- Effect: Backend and database are reachable only through intended service boundaries.

6. Secret handling through AWS-managed secret references
- Why: Avoid hardcoding sensitive credentials in task definitions.
- How: ECS backend task pulls DB password from managed secret material with scoped IAM permission.
- Effect: Lower credential exposure risk in runtime configuration.

## Local Development

### Requirements

- Docker Desktop with Docker Compose

Optional host tooling:

- Python 3.14 for direct local pytest and Alembic workflows
- Node.js 24.18.0 and npm 11.16.0 for direct frontend workflows

### Start full stack

From repository root:

```bash
docker compose up --build
```

Service endpoints:

- Postgres: 127.0.0.1:5432
- Backend: http://127.0.0.1:8000
- Frontend: http://127.0.0.1:3000

Stop:

```bash
docker compose down
```

Reset local volumes:

```bash
docker compose down -v
```

### Convenience commands

```bash
make up
make down
make test
make migrate
make revision
make logs
```

### Run tests

```bash
cd backend
source .venv/bin/activate
python -m pytest -vv ../tests
```

## Repository Layout

```text
/frontend            Next.js application
/backend             FastAPI application and migrations
/tests               Unit, API, repository, and integration tests
/infra               Terraform for AWS deployment
/docs                Architecture and supporting documentation
/prompts             Prompt templates and prompt guidance
/shared              Cross-layer shared assets and contracts
```

## Roadmap

The long-term product direction remains unchanged:

- CV and job description understanding with AI assistance
- AI-generated role-specific interview questions
- AI answer scoring and structured coaching feedback
- Personalized progression tracking and adaptive interview difficulty
- Extended interview modalities including richer simulation experiences
