#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
COMPOSE_FILE="$ROOT_DIR/docker-compose.yml"
SERVICE_NAME="postgres"
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

  echo "Docker Compose is required to manage local Postgres."
  echo "Install Docker Desktop (or docker-compose) and retry."
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

container_id() {
  compose ps -q "$SERVICE_NAME"
}

is_running() {
  local cid="$1"
  [[ -n "$cid" ]] && docker inspect -f '{{.State.Running}}' "$cid" 2>/dev/null | grep -q true
}

health_status() {
  local cid="$1"
  docker inspect -f '{{if .State.Health}}{{.State.Health.Status}}{{else}}unknown{{end}}' "$cid" 2>/dev/null
}

wait_for_healthy() {
  local cid

  for _ in {1..60}; do
    cid="$(container_id)"
    if [[ -n "$cid" ]] && is_running "$cid"; then
      if [[ "$(health_status "$cid")" == "healthy" ]]; then
        return 0
      fi
    fi
    sleep 0.5
  done

  echo "Postgres did not become healthy in time."
  return 1
}

up() {
  require_compose
  compose up -d "$SERVICE_NAME"
  wait_for_healthy

  echo ""
  echo "Local Postgres is running:"
  echo "- Host: 127.0.0.1"
  echo "- Port: 5432"
  echo "- Database: ai_interview_coach"
  echo "- User: ai_interview"
}

down() {
  require_compose
  compose stop "$SERVICE_NAME" >/dev/null
  echo "Local Postgres stopped."
}

status() {
  require_compose

  local cid
  cid="$(container_id)"

  if [[ -z "$cid" ]] || ! is_running "$cid"; then
    echo "Local Postgres is not running."
    return 0
  fi

  echo "Local Postgres running ($cid)."
  echo "Health: $(health_status "$cid")"
}

logs() {
  require_compose
  compose logs --tail=100 "$SERVICE_NAME"
}

reset() {
  require_compose
  compose down -v
  echo "Local Postgres data reset (container and volume removed)."
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
    echo "Usage: ./scripts/postgres.sh {up|down|status|logs|reset}"
    exit 1
    ;;
esac
