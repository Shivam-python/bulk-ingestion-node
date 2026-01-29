#!/usr/bin/env bash
set -e

# wait for Redis (if using local container)
function wait_for_redis() {
  echo "Waiting for Redis..."
  until nc -z "${REDIS_HOST}" "${REDIS_PORT}"; do
    sleep 0.2
  done
}

if [ -n "$REDIS_HOST" ] && [ -n "$REDIS_PORT" ]; then
  wait_for_redis
fi

exec "$@"
