@echo off

SET arg1=%1

REM Set current directory relative to this file
cd /d %~dp0

REM Execute Automation
python -m pytest --confcutdir=.\data\features --collect-only > .\logs\Automation_%arg1%.log
REM pause

REM Display Automation Report after
REM .\report\report.html