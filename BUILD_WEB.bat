@echo off
setlocal
cd /d "%~dp0"

echo ===============================================
echo PISAY FLOATING ISLANDS - V6.1 WEB BUILD
echo ===============================================
echo.

echo Installing/updating pygbag for this build...
py -m pip install --user --upgrade pygbag==0.9.4
if errorlevel 1 goto :error

echo.
echo Building browser version...
py -m pygbag --build --title "PISAY FLOATING ISLANDS" .
if errorlevel 1 goto :error

echo.
echo BUILD COMPLETE
if exist "build\web" echo Output folder: %CD%\build\web
exit /b 0

:error
echo.
echo BUILD FAILED. Read the error above.
exit /b 1
