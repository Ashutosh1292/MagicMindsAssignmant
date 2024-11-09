@echo off
docker-compose up --build -d
timeout /t 5 /nobreak
powershell.exe -Command "Start-Process 'http://127.0.0.1:8000'"