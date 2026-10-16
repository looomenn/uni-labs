#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"

if ! command -v go >/dev/null 2>&1; then
  echo "Go is required: https://go.dev/dl/" >&2
  exit 1
fi

requests="${REQUESTS_PER_CLIENT:-10000}"
port="${PORT:-8080}"
results="results/benchmarks/$(date +%Y%m%d-%H%M%S)"
tmp="$(mktemp -d)"
server_pid=""

cleanup() {
  if [[ -n "$server_pid" ]]; then
    kill "$server_pid" 2>/dev/null || true
    wait "$server_pid" 2>/dev/null || true
  fi
  rm -rf "$tmp"
}
trap cleanup EXIT


mkdir -p "$results"
go build -o "$tmp/server" ./server
go build -o "$tmp/client" ./client

for mode in memory disk; do
  "$tmp/server" -storage="$mode" -file="$tmp/counter.dat" -addr="127.0.0.1:$port" \
    >"$results/$mode-server.log" 2>&1 &
  server_pid=$!
  sleep 1

  if ! kill -0 "$server_pid" 2>/dev/null; then
    echo "Server failed. Check $results/$mode-server.log" >&2
    exit 1
  fi

  for clients in 1 2 5 10; do
    echo
    echo "+----+ $mode: $clients client(s) +----+"
    "$tmp/client" -clients="$clients" -requests="$requests" \
      -url="http://127.0.0.1:$port" 2>&1 | tee "$results/$mode-$clients.txt"
  done

  kill "$server_pid" 2>/dev/null || true
  wait "$server_pid" 2>/dev/null || true
  server_pid=""
done

echo "Done. Results: $results"
