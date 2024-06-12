@echo off
rem Batch file to convert .ui to .py using pyuic5

set UI_FILE=bike_designer.ui
set PY_FILE=dashboard.py

pyuic5 -o %PY_FILE% %UI_FILE%

echo Conversion complete.
pause
