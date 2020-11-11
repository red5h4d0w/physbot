#! /bin/bash

# Sync with GitHub repo
git fetch --all
git pull origin master

# Start the bot
python PhysBot.py
