#!/usr/bin/env bash
set -euo pipefail

GATEWAY_URL=${GATEWAY_URL:-http://localhost:8080}

function create_user() {
  curl -sS -X POST "${GATEWAY_URL}/v1/users" \
    -H 'Content-Type: application/json' \
    -d '{"name":"Jane Developer","email":"jane@example.com"}'
}

function create_order() {
  curl -sS -X POST "${GATEWAY_URL}/v1/orders" \
    -H 'Content-Type: application/json' \
    -d '{"user_id":1,"item":"starter-kit","quantity":1}'
}

function list_inventory() {
  curl -sS "${GATEWAY_URL}/v1/inventory"
}

create_user
create_order
list_inventory

echo "Seed data loaded via ${GATEWAY_URL}"
