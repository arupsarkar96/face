#!/bin/bash

set -e

APP_NAME="fastapi"
APP_DIR="$PWD"
VENV_DIR="$APP_DIR/venv"
USER=$(whoami)
PYTHON_VERSION="3.12"
PYTHON_BIN="/usr/bin/python${PYTHON_VERSION}"
DEBIAN_FRONTEND=noninteractive

echo "🔧 [0/8] Updating system and installing core packages..."
sudo apt update
sudo apt install -y software-properties-common curl build-essential libssl-dev libffi-dev \
    libpq-dev python${PYTHON_VERSION} python${PYTHON_VERSION}-venv python${PYTHON_VERSION}-dev redis-server

if ! command -v $PYTHON_BIN >/dev/null 2>&1; then
    echo "❌ Python $PYTHON_VERSION not installed correctly."
    exit 1
fi

echo "🐍 [1/8] Creating virtual environment..."
$PYTHON_BIN -m venv $VENV_DIR
source $VENV_DIR/bin/activate

echo "📦 [2/8] Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🧠 [3/8] Writing Gunicorn systemd service..."
sudo tee /etc/systemd/system/$APP_NAME.service > /dev/null <<EOF
[Unit]
Description=Gunicorn for FastAPI
After=network.target

[Service]
User=$USER
WorkingDirectory=$APP_DIR
ExecStart=$VENV_DIR/bin/gunicorn app.main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --workers 4
Restart=always
Environment=PATH=$VENV_DIR/bin

[Install]
WantedBy=multi-user.target
EOF

echo "⚙️ [4/8] Writing Celery systemd service..."
sudo tee /etc/systemd/system/celery.service > /dev/null <<EOF
[Unit]
Description=Celery Worker
After=network.target

[Service]
User=$USER
WorkingDirectory=$APP_DIR
ExecStart=$VENV_DIR/bin/celery -A app.core.celery.app worker --loglevel=info
Restart=always
Environment=PATH=$VENV_DIR/bin

[Install]
WantedBy=multi-user.target
EOF

echo "🔄 [5/8] Reloading systemd..."
sudo systemctl daemon-reload

echo "🚀 [6/8] Enabling services..."
sudo systemctl enable $APP_NAME
sudo systemctl enable celery
sudo systemctl enable redis-server

echo "✅ [7/8] Starting services..."
sudo systemctl restart redis-server
sudo systemctl restart $APP_NAME
sudo systemctl restart celery

echo "🎉 [8/8] Deployment complete!"
