@echo off
:: This script must run as Administrator

echo.
echo ========================================
echo   EduHelm Custom Domain Setup
echo ========================================
echo.

:: Check for admin rights
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running as Administrator... OK
    echo.
) else (
    echo ERROR: This script must run as Administrator!
    echo.
    echo How to run as Administrator:
    echo 1. Right-click on this file
    echo 2. Select "Run as administrator"
    echo.
    pause
    exit /b 1
)

:: Add to hosts file
echo Adding eduhelm.local to Windows hosts file...
echo.

findstr /C:"eduhelm.local" %WINDIR%\System32\drivers\etc\hosts >nul
if %errorLevel% == 0 (
    echo Custom domain already configured!
) else (
    echo # EduHelm Educational Platform - Custom Domain>> %WINDIR%\System32\drivers\etc\hosts
    echo 127.0.0.1 eduhelm.local>> %WINDIR%\System32\drivers\etc\hosts
    echo 127.0.0.1 www.eduhelm.local>> %WINDIR%\System32\drivers\etc\hosts
    echo.
    echo Successfully added custom domain!
)

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo You can now access EduHelm at:
echo    http://eduhelm.local:8000
echo.
echo Next steps:
echo 1. Start your Django server
echo 2. Open browser and go to: http://eduhelm.local:8000
echo 3. Bookmark it for easy access!
echo.
echo ========================================
echo.
pause
