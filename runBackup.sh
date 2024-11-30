#!/bin/bash

source SpotifyStatsEnv/bin/activate

pip3 install -r requirements.txt

xterm -e python SpotifyAuthorizationManager.py
xterm -e ngrok http --domain=boss-bluegill-intimate.ngrok-free.app 3000

python3 main.py

deactivate