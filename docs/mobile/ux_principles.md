# UX Principles & Navigation — dieHantar

This document captures core UX principles, navigation hierarchy, and empty state guidance.

## Core UX Principles
- Speed: Repeat orders should be accomplishable in ≤ 3 taps from the main screen (Quick Order). Prioritize common actions in primary UI.
- Real-time: Status for active trips/orders must be visible on the home/dashboard screen.
- Help-first: Access to help (chat/phone/FAQ) must be ≤ 2 taps from any active order screen.
- Progressive disclosure: Show minimal friction inputs first (quick address selection), expose advanced options only when needed.
- Accessibility-first: Use sufficient color contrast, scalable fonts, and screen reader labels for critical statuses.

## Navigation Hierarchy
Primary tabs:
- Transport
- Food
- Orders
- Wallet
- Profile

Deep links:
- /order/:order_id -> opens order detail & tracking overlay
- /track/:driver_id -> direct map tracking view

## Empty States
- No active orders: show Quick Order with recent orders list and CTA to re-order.
- No payment methods: show Add Payment button with short explanation of benefits (faster checkout).
- No nearby drivers/restaurants: show nearby service suggestions and retry button.

## Accessibility Strategy
- Color contrast: follow WCAG AA (4.5:1) for body text, AAA for large text where possible.
- Font scaling: respect OS text size settings; use rem/em scaling for internal components.
- Screen reader: provide descriptive labels for dynamic statuses ("Driver John arriving in 2 minutes").
- Focus order: ensure modal flows and forms follow logical tab order. Use ARIA landmarks on web.

```