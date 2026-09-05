@echo off
setlocal
cd /d "%~dp0"
set "ComSpec=C:\Windows\System32\cmd.exe"
set "COMSPEC=C:\Windows\System32\cmd.exe"

if not exist ".venv\Scripts\python.exe" (
  echo Creating Python environment...
  py -3 -m venv .venv
  if errorlevel 1 (
    echo Could not create .venv. Install Python 3.11+ and try again.
    pause
    exit /b 1
  )
  echo Installing backend dependencies...
  .venv\Scripts\python.exe -m pip install -r backend\requirements.txt
  if errorlevel 1 (
    echo Could not install backend dependencies.
    pause
    exit /b 1
  )
)

if not exist "frontend\node_modules" (
  echo Installing frontend dependencies...
  call npm --prefix frontend install
  if errorlevel 1 (
    echo Could not install frontend dependencies. Install Node.js 18+ and try again.
    pause
    exit /b 1
  )
)

start "Razorpay Sentinel API" cmd /k "cd /d %~dp0 && .venv\Scripts\python.exe -m uvicorn backend.main:app --reload --port 8000"
start "Razorpay Sentinel Dashboard" cmd /k "cd /d %~dp0frontend && npm run dev -- --host 127.0.0.1"

timeout /t 3 /nobreak >nul
start "" "http://127.0.0.1:5173/"
endlocal
