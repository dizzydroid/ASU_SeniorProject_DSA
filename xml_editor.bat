@echo off
REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0

REM Call Python script using the resolved script directory
python "%SCRIPT_DIR%src\cli\cli_handler.py" %*
