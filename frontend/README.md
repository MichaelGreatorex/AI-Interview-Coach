# AI Interview Coach — Frontend

Next.js 16 (App Router) frontend for the AI Interview Coach project.

## Getting Started

Copy the environment file and start the development server:

```bash
cp .env.local.example .env.local
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

The backend API must be running at the URL configured in `NEXT_PUBLIC_API_URL` (defaults to `http://localhost:8000/api/v1`).

## Pages

| Route | Description |
|-------|-------------|
| `/` | Landing page |
| `/upload` | Upload CV (PDF) and paste job description |
| `/interview/[sessionId]` | Chat-based mock interview with live AI feedback |

## Scripts

```bash
npm run dev      # Start development server
npm run build    # Production build
npm run lint     # Run ESLint
```
