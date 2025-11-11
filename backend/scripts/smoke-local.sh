#!/usr/bin/env bash
set -euo pipefail

# Start services in background (for local dev) and run health checks.
node /workspaces/dieHantar-mobile/services/auth/index.js &
PID_AUTH=$!
node /workspaces/dieHantar-mobile/services/order/index.js &
PID_ORDER=$!

# give them a moment
sleep 1

echo "Checking auth health..."
curl -sS http://localhost:3001/health || { echo "auth health failed"; kill $PID_AUTH $PID_ORDER; exit 1; }

echo "Checking order health..."
curl -sS http://localhost:3002/health || { echo "order health failed"; kill $PID_AUTH $PID_ORDER; exit 1; }

echo "Both services healthy. Cleaning up..."
kill $PID_AUTH $PID_ORDER
