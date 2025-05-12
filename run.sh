#!/bin/bash

# Start Gunicorn for FastAPI
echo "Starting Gunicorn for FastAPI..."
gunicorn app.main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --workers 1 &

# Start Celery worker
echo "Starting Celery worker..."
celery -A app.core.celery.app worker --loglevel=info &

# Wait for both processes to keep the script running
wait
