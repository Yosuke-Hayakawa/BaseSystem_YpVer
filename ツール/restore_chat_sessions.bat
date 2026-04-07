@echo off
chcp 65001 >nul 2>&1
echo ============================================================
echo   VS Code Copilot Chat セッション復旧ツール
echo ============================================================
echo.
echo ※ VS Codeを完全に閉じた状態で実行してください
echo.

python "%~dp0restore_chat_sessions.py"

echo.
echo ============================================================
if %ERRORLEVEL% EQU 0 (
    echo   正常終了しました
) else (
    echo   エラーが発生しました（終了コード: %ERRORLEVEL%）
)
echo ============================================================
echo.
pause
