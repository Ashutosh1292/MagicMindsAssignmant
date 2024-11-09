#!/bin/bash

# Run docker-compose to build and start the services in the background
docker-compose up --build &

# Wait for a few seconds to allow the service to start (adjust time as needed)
sleep 3

# Open the default browser to access the application
# Linux
xdg-open http://127.0.0.1:8000 2>/dev/null ||
# macOS
open http://127.0.0.1:8000 2>/dev/null ||
# Windows (using PowerShell)
powershell.exe start http://127.0.0.1:8000
