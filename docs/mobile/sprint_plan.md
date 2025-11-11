# Sprint Plan (Initial) — dieHantar

This plan maps the priority items (see O. Prioritas Sprint Awal) into a 4-week iteration plan for an initial team.

## Sprint 0 (Setup, 1 week)
- Finalize personas & journeys (docs/mobile/personas.md, docs/mobile/journeys.md)
- Project scaffolding: repositories interfaces, DI setup, base ViewModel pattern
- Add design tokens (design/design_tokens.json) and integrate into frontend/starter
- Setup CI skeleton: lint + tests

## Sprint 1 (Core flows, 2 weeks)
- Transport: basic booking (pickup, destination, fare estimate) + fare calculation use case
- Food: browse restaurants, add to cart, place order (simple cart, one-restaurant per order)
- Real-time: polling-based driver location + tracking view; fallback to polling
- Payment: internal wallet simulation and toggles for gateway
- Analytics: emit core events (AppLaunch, RideRequested, FoodOrderCreated)

## Sprint 2 (Hardening & observability, 2 weeks)
- Integrate WebSocket for real-time updates (3–5s interval), smoothing client-side
- Add offline cache for recent orders and static map tiles
- Implement token rotation basics and secure local storage
- Add basic rate limiting and monitoring on backend endpoints
- QA: integration tests for booking and order lifecycle; publish to internal beta

## Acceptance Criteria (for MVP)
- Passenger can place a ride and track driver until completion
- Passenger can order food from one restaurant, track order status, and receive proof-of-delivery
- Basic payments flow using internal wallet works end-to-end
- Event analytics for core events appear in backend logs

## Next Steps
- Add Redis + caching for dashboard stats
- Add feature flag infrastructure for staged rollouts
- Expand UI library and accessibility audit

```