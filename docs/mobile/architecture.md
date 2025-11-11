# Mobile Architecture — dieHantar

This document describes the recommended mobile architecture and technical constraints to support both Transport and Food product lines.

## High level choice
- Adopt Clean Architecture (domain-driven) combined with MVVM for presentation. This keeps UI, domain, and data layers decoupled and testable.

## Layers
- Presentation (UI + ViewModel): platform-specific UI (Flutter/React Native/Native) and ViewModels exposing observable state.
- Domain (Use Cases / Interactors): business rules (CreateRideOrder, CreateDeliveryOrder, CalculateFare, ApplyPromo).
- Data (Repositories + Sources): repository interfaces (UserRepository, OrderRepository, LocationRepository, PaymentRepository). Implementations for network, cache, and local DB.
- Infrastructure: DI container, network clients, persistence (SQLite), real-time channels.

## Key Interfaces
- UserRepository: getCurrentUser(), login(), signup(), refreshToken(), updateProfile()
- OrderRepository: createOrder(), getOrder(), listOrders(), cancelOrder(), trackOrder()
- LocationRepository: getCurrentLocation(), reverseGeocode(), suggestedPickupPoints()
- PaymentRepository: listMethods(), charge(), refund(), topUp()

## Real-time & Mapping
- Abstract map provider via IMapAdapter with implementations for Google/Mapbox/OSM.
- Real-time via WebSocket or MQTT adapter (IRealtimeAdapter) that emits driver positions, order events.

## Dependency Injection
- Use platform-appropriate DI (Hilt for Android, Swift patterns for iOS, Provider/GetIt for Flutter) to inject repositories and adapters into ViewModels.

## Testing
- Each repository interface must have an in-memory/mock implementation for unit and UI tests.
- Use contract tests to validate repository behavior against network stubs.

## Modularity
- Keep Transport and Food modules independent at UI and feature-level, but share Domain models for Orders and Payment primitives.

```