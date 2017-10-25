#!/bin/bash

./utils/mangocore-linux-amd64.x --case ./samples/main2.json --identity ./utils/identity.json --start 5
sleep 5
python utils/bot.py
