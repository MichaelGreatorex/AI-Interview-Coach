# Prompts

This directory is reserved for prompt templates and prompt-governance assets as AI capabilities are expanded.

The current release already includes AI-assisted document understanding logic in backend services. Prompt artifacts can be formalized here as templates are externalized and versioned.

## Intended contents

- Document understanding prompts
- Question generation prompts
- Answer evaluation prompts
- Coaching and feedback prompts

## Secure by Design for prompt assets

1. Minimize sensitive data in prompt context
- Why: Candidate documents may contain personal data.
- How: Pass only required fields and redact where feasible.
- Effect: Reduced privacy and accidental leakage risk.

2. Explicit output contracts
- Why: Unstructured model output can break downstream logic.
- How: Define strict schema expectations in prompt instructions and validate responses server-side.
- Effect: Safer integration and predictable failure handling.

3. Versioned prompt changes
- Why: Prompt edits can silently change behavior.
- How: Keep prompts in source control with change rationale and related tests.
- Effect: Auditability and faster rollback of regressions.

4. Deterministic fallback paths
- Why: External AI dependencies can fail or time out.
- How: Keep non-AI workflow paths operable and return clear API errors.
- Effect: Better availability and user trust during degraded AI service.
