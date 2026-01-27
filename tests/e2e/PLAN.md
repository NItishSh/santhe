# E2E Testing Plan (Playwright)

## 1. Goal
Verify critical user journeys on the deployed Microservices application (`http://localhost:8080`) without manual intervention.

## 2. Scope (Smoke Tests)
We will implement "Happy Path" tests for the following flows:
1.  **Public Home Page**: Verify page loads and critical elements (Header, "Santhe" branding) exist.
2.  **Product Catalog**: Verify products are displayed (fetched from `product-catalog-service`).
3.  **Authentication UI**: Verify Login/Signup forms appear (functional test depends on `user-service` seeding).

## 3. Architecture
- **Tool**: Playwright (TypeScript)
- **Location**: `tests/e2e/` (Root-level, decoupled from `web` service)
- **Target environment**: Docker/Kind cluster (`localhost:8080`)
- **Headless**: Yes (CI-ready)

## 4. Implementation Steps
1.  Initialize `tests/e2e` with `package.json`.
2.  Install `@playwright/test` and `typescript`.
3.  Configure `playwright.config.ts` for minimal setup (Chromium only, strict timeouts).
4.  Write `tests/e2e/smoke.spec.ts`.
5.  Execute and verify.

## 5. Success Criteria
- [ ] `npm test` passes in `tests/e2e`.
- [ ] Screenshots captured on failure.
