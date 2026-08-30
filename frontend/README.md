# Frontend

This package provides the interview client for AI Interview Coach.

## Current Functionality

The application runs a complete multi-stage interview workflow:

1. Upload stage
- Upload CV and job description files.
- Sends multipart form data to backend document-processing endpoint.

2. Review stage
- Displays extracted text for both documents.
- Allows user corrections before interview starts.
- Persists edits via backend document update endpoint.

3. Interview stage
- Displays current question.
- Submits answers and advances using backend progression response.

4. Complete stage
- Shows completion view.
- Ends and deletes the interview session on user action.

## API Integration

The frontend integrates with these backend paths under API base URL:

- POST /interviews
- PATCH /interviews/{interview_session_id}/documents/{document_id}
- POST /interviews/{interview_session_id}/start
- POST /sessions/{interview_session_id}/responses
- DELETE /sessions/{interview_session_id}

Base URL is configured through NEXT_PUBLIC_API_BASE_URL.

## Secure by Design

1. Explicit request timeouts for long-running actions
- Why: Prevent hanging user operations and reduce retry storms.
- How: AbortController-based timeout controls in document processing and response submission.
- Effect: Predictable failure paths and better resilience under network degradation.

2. Controlled stage transitions
- Why: Prevent invalid UI states and accidental repeated submissions.
- How: Busy-state guards and submission locks around critical actions.
- Effect: Lower risk of duplicate requests and race-condition style UX failures.

3. Server-authoritative interview progression
- Why: Client state should not be trusted for interview flow decisions.
- How: Next question and completion status are always derived from backend responses.
- Effect: Tampering resistance and consistent business logic.

## Run locally

```bash
npm install
npm run dev
```

Default local URL: http://localhost:3000

## Scripts

- npm run dev
- npm run build
- npm run start
- npm run lint
