#!/usr/bin/env bash
set -euo pipefail

# Start docker-compose and run a small integration flow:
# 1) start services (with postgres)
# 2) register a user
# 3) login user
# 4) create an order
# 5) fetch health endpoints

echo "Starting docker-compose..."
docker-compose up -d --build

# wait for services
for i in {1..30}; do
  if curl -sSf http://localhost:3001/health >/dev/null && curl -sSf http://localhost:3002/health >/dev/null; then
    echo "services healthy"; break
  fi
  sleep 2
done

# register
echo "Registering test user..."
resp=$(curl -s -X POST http://localhost:3001/auth/register -H 'Content-Type: application/json' -d '{"username":"tester","password":"secret"}')
echo "register response: $resp"

# login
echo "Logging in test user..."
resp=$(curl -s -X POST http://localhost:3001/auth/login -H 'Content-Type: application/json' -d '{"username":"tester","password":"secret"}')
echo "login response: $resp"

# create order (use userId 1 for demo)
echo "Creating order..."
resp=$(curl -s -X POST http://localhost:3002/orders -H 'Content-Type: application/json' -d '{"userId":1,"items":[{"productId":1,"qty":2}]}')
echo "create order response: $resp"

echo "Integration flow complete. Tearing down..."
docker-compose down -v

echo "Done."
