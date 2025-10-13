#!/usr/bin/env bash
set -euo pipefail

if command -v gofmt >/dev/null; then
  gofmt -w $(find services -name '*.go' -print)
fi

if command -v black >/dev/null; then
  black services/orders
fi

if command -v npm >/dev/null; then
  npm --prefix apps/web run format
fi

