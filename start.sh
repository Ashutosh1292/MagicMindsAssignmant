#!/bin/bash

# Start Docker containers in the background
docker-compose up --build -d

# Wait for 5 seconds to ensure containers have started
sleep 2

# Open the URL in the default web browser
xdg-open http://127.0.0.1:8000
