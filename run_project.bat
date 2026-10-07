
@echo off
echo ===================================================
echo   Starting Shopper Conversion Simulator 🚀
echo ===================================================

echo [1/2] Starting Backend Server...
start cmd /k "cd backend && python main.py"

echo [2/2] Starting Frontend Client...
start cmd /k "cd frontend/data_mining && npm run dev"

echo.
echo Both servers are starting in new windows!
echo Please wait a moment, then open http://localhost:5173
echo.
pause
