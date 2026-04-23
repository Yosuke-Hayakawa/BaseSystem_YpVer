@echo off
pushd "%~dp0"
python capl_doc_gui.py
if errorlevel 1 (
    echo.
    echo Pythonが見つかりません。Pythonをインストールしてください。
    pause
)
popd