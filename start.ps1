Start-Process "docker-compose" -ArgumentList "up --build"
Start-Sleep -Seconds 1
Start-Process "http://127.0.0.1:8000"
