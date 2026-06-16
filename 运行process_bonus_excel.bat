@echo off
cd /d "%~dp0"
set PROCESS_BONUS_EXCEL_NO_PAUSE=1
python process_bonus_excel.py
pause
