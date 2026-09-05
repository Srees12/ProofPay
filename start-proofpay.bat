@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"
set "ComSpec=C:\Windows\System32\cmd.exe"
set "COMSPEC=C:\Windows\System32\cmd.exe"
set "API_URL=http://127.0.0.1:8000"
set "APP_URL=http://127.0.0.1:5173/"

echo ========================================
echo PROOFPAY
echo Evidence. Intelligence. Resolution.
echo ========================================
if not exist ".venv\Scripts\python.exe" (
  echo [setup] Creating Python environment...
  py -3 -m venv .venv
  if errorlevel 1 goto :fail
  echo [setup] Installing backend dependencies...
  .venv\Scripts\python.exe -m pip install -r backend\requirements.txt
  if errorlevel 1 goto :fail
)
if not exist "frontend\node_modules" (
  echo [setup] Installing frontend dependencies...
  call npm --prefix frontend install
  if errorlevel 1 goto :fail
)
echo [1/4] Starting backend...
start "ProofPay API" cmd /k "cd /d %~dp0 && set ComSpec=C:\Windows\System32\cmd.exe && set COMSPEC=C:\Windows\System32\cmd.exe && .venv\Scripts\python.exe -m uvicorn backend.main:app --reload --port 8000"
echo [2/4] Waiting for API...
for /l %%i in (1,1,30) do (
  powershell -NoProfile -ExecutionPolicy Bypass -Command "try { Invoke-WebRequest -UseBasicParsing -Uri '%API_URL%/api/health' -TimeoutSec 1 | Out-Null; exit 0 } catch { exit 1 }"
  if not errorlevel 1 goto api_ready
  timeout /t 1 /nobreak >nul
)
echo API did not become ready in 30 seconds.
goto :fail
:api_ready
echo       API operational
echo [3/4] Starting frontend...
start "ProofPay Dashboard" cmd /k "cd /d %~dp0frontend && set ComSpec=C:\Windows\System32\cmd.exe && set COMSPEC=C:\Windows\System32\cmd.exe && npm run dev -- --host 127.0.0.1"
echo [4/4] Waiting for frontend...
for /l %%i in (1,1,30) do (
  powershell -NoProfile -ExecutionPolicy Bypass -Command "try { Invoke-WebRequest -UseBasicParsing -Uri '%APP_URL%' -TimeoutSec 1 | Out-Null; exit 0 } catch { exit 1 }"
  if not errorlevel 1 goto frontend_ready
  timeout /t 1 /nobreak >nul
)
echo Frontend did not become ready in 30 seconds.
goto :fail
:frontend_ready
echo       Dashboard operational
start "" "%APP_URL%"
echo.
echo ProofPay is running: %APP_URL%
echo API health: %API_URL%/api/health
echo Keep the two service windows open while using the application.
goto :done
:fail
echo.
echo Startup failed. Check the service window and prerequisites (Python 3.11+, Node.js 18+).
pause
exit /b 1
:done
endlocal
