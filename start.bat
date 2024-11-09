@echo off
docker-compose up --build
powershell.exe -ExecutionPolicy Bypass -File .\start.ps1
