dieHantar - Architecture overview (ASCII diagram)

Client (Mobile)
   |  HTTPS / WebSocket
   v
API Gateway / BFF
   |  REST/gRPC
   v
+----------------------+        +-----------------------+
|  Auth Service        | <----> |  Order Service         |
|  (JWT, user mgmt)    |        |  (create, status)      |
+----------------------+        +-----------------------+
   |                               |
   v                               v
 PostgreSQL                     Message Broker (Rabbit/Kafka)
   |
   v
 Object Storage (S3)

Notes:
- Mobile can be implemented with Flutter or React Native (Expo) — see `mobile/` placeholder.
- Services are Node.js Express stubs under `services/`.
- k8s manifests in `infra/k8s` are minimal examples for local testing.
- OpenAPI skeleton under `openapi/` contains minimal endpoints for auth and orders.

Next steps:
- Replace stub services with real implementations (DB, migrations, env config).
- Add CI pipeline (GitHub Actions) to build images and push to registry.
- Add real secrets management and ingress config for API gateway.
