#!/bin/bash
set -e

echo "⏳ Waiting for DB"
until pg_isready -h "$CHAT_ACC_MNGR_DB_HOST" -p "$CHAT_ACC_MNGR_PORT" -U "$CHAT_ACC_MNGR_USER"; do
  sleep 1
done
echo "📦 Applying migrations"
alembic upgrade head

echo "🚀 Start App"
exec "$@"