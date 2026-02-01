@echo off
echo Starting Chemical Equipment Visualizer...

REM Start Backend
start "Backend Server" cmd /k "cd /d %~dp0backend && python manage.py runserver"

REM Start Web Frontend
start "Web Frontend" cmd /k "cd /d %~dp0web-frontend && npm run dev"

REM Start Desktop Frontend
echo Waiting for backend to initialize...
timeout /t 5
start "Desktop App" cmd /k "cd /d %~dp0desktop-frontend && python main.py"

echo All services started!
echo 1. Backend: http://127.0.0.1:8000/
echo 2. Web App: http://localhost:3000/
echo 3. Desktop App: Launched in new window.
pause
