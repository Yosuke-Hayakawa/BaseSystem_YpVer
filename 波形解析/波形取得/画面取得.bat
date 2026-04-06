@echo off
chcp 65001 > nul
cd /d "%~dp0スクリプト"
python capture_screen.py %*
