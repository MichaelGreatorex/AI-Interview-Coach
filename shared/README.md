# Shared

This directory is reserved for cross-layer shared contracts and constants as the platform evolves.

Current implementation keeps contracts close to each runtime:

- Backend Pydantic schemas under backend app schemas
- Frontend TypeScript interfaces under frontend feature models and types

As shared contract complexity grows, this directory can host generated or manually curated shared definitions.

## Secure by Design for shared contracts

1. Contract minimization
- Why: Overexposed payloads increase accidental data leakage.
- How: Share only fields needed by both layers.
- Effect: Smaller attack surface and clearer API boundaries.

2. Backward-compatible evolution
- Why: Breaking contract changes can create unsafe client workarounds.
- How: Version changes and deprecate fields gradually.
- Effect: Safer rollout and fewer production regressions.

3. Consistent validation semantics
- Why: Divergent validation between frontend and backend creates trust gaps.
- How: Keep field constraints aligned and test contract expectations.
- Effect: Lower risk of malformed data entering core services.
