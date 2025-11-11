# Performance & Load Testing Plan

## Targets
- API latency p95 < 1.5s for core endpoints
- Throughput goal: 200 RPS sustained on product listing

## Tooling
- Locust planned (locustfile_001.py placeholder) for scenario scripting
- Future: k6 for browser-like flows

## Scenarios (Initial)
1. Anonymous product listing pagination
2. Authenticated category CRUD burst
3. Mixed read/write (products create + list)
4. Health + metrics endpoint under load

## Metrics to Capture
- Response time percentiles (p50, p90, p95, p99)
- Error rate (% 4xx + 5xx)
- Throughput (requests / second)
- Redis hit ratio (once caching metrics added)

## Environment Notes
Run tests against a staging deployment mirroring production config (indices, caching, rate limits).

## Next Steps
- Implement locustfile_001.py with user classes
- Integrate Prometheus metrics for internal instrumentation
- Add synthetic trace IDs for correlation
