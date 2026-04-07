@echo off
chcp 65001 >nul
echo CRAMAS NG解析開始
echo.
python "%~dp0scripts\ng_check.py" %*
echo.
pause
