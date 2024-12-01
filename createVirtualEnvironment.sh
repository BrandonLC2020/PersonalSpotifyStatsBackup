#!/bin/bash

python3 -m venv SpotifyStatsEnv

source SpotifyStatsEnv/bin/activate

pip3 install -r requirements.txt

deactivate