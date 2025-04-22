#!/usr/bin/env bash
set -e

alembic upgrade head
uvicorn dio_blog.main:app --host 0.0.0.0 --port $PORT
