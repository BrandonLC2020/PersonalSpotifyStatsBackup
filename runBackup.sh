#!/bin/bash

# Load environment variables from .env file
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

source SpotifyStatsEnv/bin/activate

xterm -e python3 SpotifyAuthorizationManager.py
xterm -e ngrok http --domain="$NGROK_DOMAIN" "$NGROK_PORT"

python3 main.py

deactivate