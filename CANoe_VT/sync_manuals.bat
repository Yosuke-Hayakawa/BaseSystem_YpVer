@echo off
chcp 65001 >nul
echo ============================================================
echo  CANoe/VTシステム マニュアル同期
echo ============================================================
echo.

set "SRC=\\jikken-sv05\El\共通\05ソフトG\017_技術の棚入れ\格納先フォルダ\064_GithubCopilot手順書\VTシステムマニュアル.md"
set "DST=%~dp0マニュアル"

echo ソース: %SRC%
echo 同期先: %DST%
echo.

REM /E: サブフォルダ含む  /XD: 除外ディレクトリ  /R:3 W:5: リトライ
REM /MIR は使わない（ローカルのみのファイルを消さないため）
robocopy "%SRC%" "%DST%" /E /XD __pycache__ .github /R:3 /W:5 /NP /NDL /NFL

if %ERRORLEVEL% LEQ 7 (
    echo.
    echo [OK] 同期完了
) else (
    echo.
    echo [ERROR] 同期に失敗しました (exit code: %ERRORLEVEL%)
)

echo.
pause
