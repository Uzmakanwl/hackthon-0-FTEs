@echo off
REM AI Employee - Bronze Tier Startup Script for Windows
REM This script starts both the File Watcher and Orchestrator

echo ============================================
echo AI Employee - Bronze Tier
echo ============================================
echo.

REM Get the script directory
set SCRIPT_DIR=%~dp0
set VAULT_DIR=%SCRIPT_DIR%..

REM Create DropFolder if it doesn't exist
if not exist "%VAULT_DIR%\DropFolder" (
    mkdir "%VAULT_DIR%\DropFolder"
    echo Created DropFolder: %VAULT_DIR%\DropFolder
)

echo Vault Directory: %VAULT_DIR%
echo Drop Folder: %VAULT_DIR%\DropFolder
echo.

REM Start File Watcher in a new window
echo Starting File System Watcher...
start "AI Employee - File Watcher" cmd /k "cd /d %SCRIPT_DIR% && echo File Watcher Started && python filesystem_watcher.py "%VAULT_DIR%" "%VAULT_DIR%\DropFolder""

REM Wait a moment for watcher to start
timeout /t 2 /nobreak >nul

REM Start Orchestrator in current window
echo Starting Orchestrator...
echo.
cd /d %SCRIPT_DIR%
python orchestrator.py "%VAULT_DIR%"

echo.
echo ============================================
echo AI Employee Stopped
echo ============================================
