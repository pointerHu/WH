@echo off
setlocal
wsl -d Ubuntu-22.04 --exec /usr/bin/python3 /home/admin/projects/WH/ka-gzsl-demo/scripts/start_or_check.py
if errorlevel 1 (
  pause
  exit /b 1
)
start "" "http://127.0.0.1:8765"
endlocal
