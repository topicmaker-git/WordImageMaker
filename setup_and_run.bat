@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

:: Word Image Maker Ver.2 - Windows用一括セットアップ・起動スクリプト
:: 使い方: setup_and_run.bat

title Word Image Maker Ver.2 - セットアップ

echo.
echo 🎨 Word Image Maker Ver.2 - セットアップ・起動スクリプト
echo ==================================================
echo.

:: 1. Python環境チェック
echo ℹ️  Python環境をチェック中...
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python 3が見つかりません。Python 3.8以上をインストールしてください。
    echo    https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ℹ️  Python !PYTHON_VERSION! を検出しました

:: Python 3.8以上かチェック
python -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" > nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python 3.8以上が必要です。現在: !PYTHON_VERSION!
    pause
    exit /b 1
)
echo ✅ Python バージョン要件を満たしています

:: 2. 仮想環境のチェック・作成
echo ℹ️  仮想環境をチェック中...
if not exist "venv" (
    echo ℹ️  仮想環境を作成中...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ❌ 仮想環境の作成に失敗しました
        pause
        exit /b 1
    )
    echo ✅ 仮想環境を作成しました
) else (
    echo ℹ️  仮想環境が既に存在します
)

:: 3. 仮想環境の有効化
echo ℹ️  仮想環境を有効化中...
call venv\Scripts\activate
if %errorlevel% neq 0 (
    echo ❌ 仮想環境の有効化に失敗しました
    pause
    exit /b 1
)
echo ✅ 仮想環境を有効化しました

:: 4. 依存関係のインストール
echo ℹ️  依存関係をインストール中...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ 依存関係のインストールに失敗しました
    pause
    exit /b 1
)
echo ✅ 依存関係のインストールが完了しました

:: 5. 必要なディレクトリの作成
echo ℹ️  必要なディレクトリを作成中...
if not exist "output" mkdir output
if not exist "output\images" mkdir output\images
if not exist "templates" mkdir templates
if not exist "static" mkdir static
if not exist "static\css" mkdir static\css
if not exist "static\js" mkdir static\js
echo ✅ ディレクトリ構造を確認しました

:: 6. ポートチェック
echo ℹ️  ポート 5000 の使用状況をチェック中...
netstat -ano | findstr :5000 > nul 2>&1
if %errorlevel% equ 0 (
    echo ⚠️  ポート 5000 が既に使用されています
    echo    既存のプロセスを停止してから再実行してください
    pause
)

:: 7. 設定ファイルの確認
echo ℹ️  設定ファイルをチェック中...
if not exist "app.py" (
    echo ❌ app.py が見つかりません
    pause
    exit /b 1
)
echo ✅ アプリケーションファイルを確認しました

:: 8. 起動前の最終確認
echo ℹ️  起動前の最終確認...
echo.
echo 📋 セットアップ完了情報:
for /f "tokens=2" %%i in ('python --version') do echo    • Python: %%i
echo    • 仮想環境: 有効
echo    • 依存関係: インストール済み
echo    • ポート: 5000 (利用可能)
echo    • URL: http://localhost:5000
echo.
echo ⚠️  OpenAI API Key が必要です。事前に準備してください。
echo    https://platform.openai.com/api-keys
echo.

set /p response="サーバーを起動しますか？ [Y/n]: "
if /i "!response!"=="n" (
    echo.
    echo ℹ️  セットアップが完了しました。手動で起動する場合:
    echo    venv\Scripts\activate
    echo    python app.py
    pause
    exit /b 0
)

:: 9. サーバー起動
echo.
echo ℹ️  Word Image Maker Ver.2 を起動中...
echo.
echo ✅ 🚀 サーバーを起動しました！
echo ℹ️  ブラウザで http://localhost:5000 にアクセスしてください
echo ℹ️  停止するには Ctrl+C を押してください
echo.

:: アプリケーション起動
python app.py