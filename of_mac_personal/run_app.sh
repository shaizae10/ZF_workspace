#!/bin/bash
source ../../venv/bin/activate
python3 ../app.py &
open -a Safari http://127.0.0.1:8080
