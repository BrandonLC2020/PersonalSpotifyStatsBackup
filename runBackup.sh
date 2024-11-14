#!/bin/bash

xterm -e python SpotifyAuthorizationManager.py
xterm -e ngrok http --domain=boss-bluegill-intimate.ngrok-free.app 3000

python main.py
