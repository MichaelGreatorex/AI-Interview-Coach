#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
COMPOSE_FILE="$ROOT_DIR/docker-compose.yml"
COMPOSE_CMD=()

set_compose_cmd() {
  if command -v docker-compose >/dev/null 2>&1; then
    COMPOSE_CMD=(docker-compose)
    return
  fi

  if command -v docker >/dev/null 2>&1; then
    COMPOSE_CMD=(docker compose)
    return
  fi

  echo "Docker Compose is required. Install Docker Desktop (or docker-compose) and retry."
  exit 1
}

compose() {
  "${COMPOSE_CMD[@]}" -f "$COMPOSE_FILE" "$@"
}

require_compose() {
  set_compose_cmd

  if [[ ! -f "$COMPOSE_FILE" ]]; then
    echo "Compose file not found: $COMPOSE_FILE"
    exit 1
  fi
}

up() {
  require_compose
  compose up --build -d
}

down() {
  require_compose
  compose down
}

status() {
  require_compose
  compose ps
}

logs() {
  require_compose
  compose logs --tail=100
}

reset() {
  require_compose
  compose down -v
}

case "${1:-}" in
  up)
    up
    ;;
  down)
    down
    ;;
  status)
    status
    ;;
  logs)
    logs
    ;;
  reset)
    reset
    ;;
  *)
    echo "Usage: ./scripts/dev-stack.sh {up|down|status|logs|reset}"
    exit 1
    ;;
esac
