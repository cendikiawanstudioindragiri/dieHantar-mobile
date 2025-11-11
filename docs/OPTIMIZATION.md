# Per-page Optimization Checklist

Use this checklist when reviewing or building each page/screen.

## Above-the-fold
- Keep TTFB low (<200ms). Remove N+1, add indexes, cache static.
- Inline critical CSS; defer non-critical JS; lazy-load images/components.

## Assets
- Images: responsive sizes, WebP/AVIF, width/height attributes, preload hero.
- Fonts: preload critical, font-display: swap, limit variants.
- CSS/JS: code-split per route, tree-shake, drop unused deps.

## Data & caching
- Pagination (limit 20–50), filters; ETag/Last-Modified for GETs.
- SWR pattern on clients; debounce search; cancel stale requests.

## Interaction
- Avoid long tasks (>50ms); throttle scroll/resize; passive listeners.
- Accessible focus states; 44px min target size.

## Accessibility
- Single H1; labels; aria-*; keyboard navigation; contrast ≥ 4.5:1.

## SEO (web)
- Unique title/meta; canonical; structured data; sitemap; robots hygiene.

## Security
- CSP, HSTS, X-Frame-Options; CSRF for forms; escape by default.
- Rate limit auth; store JWT securely; validate inputs.

## Observability
- Track Core Web Vitals (LCP/CLS/INP); frontend error logging; event analytics.

## Flutter specifics
- const widgets; avoid rebuilds; list virtualization; cached images.
- Offload heavy work to isolates; DevTools to profile.

## FastAPI specifics
- Add indexes for common filters; prefetch relations; trim response models.
- Enable compression; tune workers; strict CORS.
