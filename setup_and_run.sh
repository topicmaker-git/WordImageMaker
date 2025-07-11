#!/bin/bash

# Word Image Maker Ver.2 - 一括セットアップ・起動スクリプト
# 使い方: ./setup_and_run.sh

set -e  # エラーが発生したらスクリプトを停止

# 色付きメッセージ用の関数
print_success() {
    echo -e "\033[32m✅ $1\033[0m"
}

print_info() {
    echo -e "\033[34mℹ️  $1\033[0m"
}

print_error() {
    echo -e "\033[31m❌ $1\033[0m"
}

print_warning() {
    echo -e "\033[33m⚠️  $1\033[0m"
}

print_header() {
    echo -e "\033[1;36m"
    echo "🎨 Word Image Maker Ver.2 - セットアップ・起動スクリプト"
    echo "=================================================="
    echo -e "\033[0m"
}

# メイン処理開始
print_header

# 1. Python環境チェック
print_info "Python環境をチェック中..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3が見つかりません。Python 3.8以上をインストールしてください。"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
print_info "Python ${PYTHON_VERSION} を検出しました"

# Python 3.8以上かチェック
if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    print_success "Python バージョン要件を満たしています"
else
    print_error "Python 3.8以上が必要です。現在: ${PYTHON_VERSION}"
    exit 1
fi

# 2. 仮想環境のチェック・作成
print_info "仮想環境をチェック中..."
if [ ! -d "venv" ]; then
    print_info "仮想環境を作成中..."
    python3 -m venv venv
    print_success "仮想環境を作成しました"
else
    print_info "仮想環境が既に存在します"
fi

# 3. 仮想環境の有効化
print_info "仮想環境を有効化中..."
source venv/bin/activate
print_success "仮想環境を有効化しました"

# 4. 依存関係のインストール
print_info "依存関係をインストール中..."
if pip install -r requirements.txt; then
    print_success "依存関係のインストールが完了しました"
else
    print_error "依存関係のインストールに失敗しました"
    exit 1
fi

# 5. 必要なディレクトリの作成
print_info "必要なディレクトリを作成中..."
mkdir -p output/images
mkdir -p templates static/css static/js
print_success "ディレクトリ構造を確認しました"

# 6. ポートチェック
print_info "ポート 5000 の使用状況をチェック中..."
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    print_warning "ポート 5000 が既に使用されています"
    print_info "既存のプロセスを停止しますか？ [y/N]"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        print_info "ポート 5000 を使用しているプロセスを停止中..."
        lsof -ti:5000 | xargs kill -9 2>/dev/null || true
        sleep 2
        print_success "プロセスを停止しました"
    else
        print_error "ポート 5000 が使用中のため起動できません"
        exit 1
    fi
fi

# 7. 設定ファイルの確認
print_info "設定ファイルをチェック中..."
if [ -f "app.py" ]; then
    print_success "アプリケーションファイルを確認しました"
else
    print_error "app.py が見つかりません"
    exit 1
fi

# 8. 起動前の最終確認
print_info "起動前の最終確認..."
echo ""
echo "📋 セットアップ完了情報:"
echo "   • Python: $(python3 --version)"
echo "   • 仮想環境: $(which python)"
echo "   • 依存関係: インストール済み"
echo "   • ポート: 5000 (利用可能)"
echo "   • URL: http://localhost:5000"
echo ""

print_warning "OpenAI API Key が必要です。事前に準備してください。"
print_info "https://platform.openai.com/api-keys"
echo ""

print_info "サーバーを起動しますか？ [Y/n]"
read -r response
if [[ "$response" =~ ^[Nn]$ ]]; then
    print_info "セットアップが完了しました。手動で起動する場合:"
    echo "   source venv/bin/activate"
    echo "   python3 app.py"
    exit 0
fi

# 9. サーバー起動
print_info "Word Image Maker Ver.2 を起動中..."
echo ""
print_success "🚀 サーバーを起動しました！"
print_info "ブラウザで http://localhost:5000 にアクセスしてください"
print_info "停止するには Ctrl+C を押してください"
echo ""

# アプリケーション起動
python3 app.py