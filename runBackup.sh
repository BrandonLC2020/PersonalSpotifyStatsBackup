#!/bin/bash

source SpotifyStatsEnv/bin/activate

xterm -e python3 SpotifyAuthorizationManager.py
xterm -e ngrok http --domain=boss-bluegill-intimate.ngrok-free.app 3000

python3 main.py

deactivate