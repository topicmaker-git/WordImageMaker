# Word Image Maker Ver.2 - セットアップガイド

## 🚀 初心者向け簡単セットアップ

### Linux / macOS 用
```bash
# 1. プロジェクトをクローン
git clone <your-private-repo-url>
cd wordImageMaker

# 2. 一括セットアップ・起動
./setup_and_run.sh
```

### Windows 用
```cmd
# 1. プロジェクトをクローン
git clone <your-private-repo-url>
cd wordImageMaker

# 2. 一括セットアップ・起動
setup_and_run.bat
```

## 📋 自動セットアップ内容

スクリプトが以下を自動実行します：

1. **Python環境チェック**
   - Python 3.8以上の確認
   - バージョン表示

2. **仮想環境セットアップ**
   - `venv` の作成・有効化
   - システム環境への影響なし

3. **依存関係インストール**
   - `requirements.txt` から自動インストール
   - 必要なPythonパッケージの準備

4. **ディレクトリ構造作成**
   - 出力フォルダの準備
   - 必要なディレクトリの作成

5. **ポートチェック**
   - ポート5000の使用状況確認
   - 競合プロセスの停止（Linux/macOS）

6. **アプリケーション起動**
   - Flask サーバーの起動
   - `http://localhost:5000` でアクセス可能

## 🔧 手動セットアップ（上級者向け）

```bash
# 仮想環境作成
python3 -m venv venv

# 仮想環境有効化
source venv/bin/activate  # Linux/macOS
# または
venv\Scripts\activate     # Windows

# 依存関係インストール
pip install -r requirements.txt

# アプリケーション起動
python3 app.py
```

## 🎯 初回利用時の設定

1. **OpenAI API Key の準備**
   - https://platform.openai.com/api-keys で取得
   - 十分な残高があることを確認

2. **ブラウザでアクセス**
   - `http://localhost:5000` を開く
   - API Key を入力（自動保存されます）

3. **英単語を入力**
   - 複数単語は改行区切り
   - `単語#補足情報` で意味を指定可能

## 📱 社内展開時の注意点

### IT管理者向け
- Python 3.8以上の事前インストール
- 社内プロキシ環境での `pip` 設定
- ファイアウォール設定（ポート5000）

### エンドユーザー向け
- **簡単**: セットアップスクリプトを実行するだけ
- **安全**: システムPythonに影響しない仮想環境
- **便利**: API Key は自動保存・復元

## 🛠️ トラブルシューティング

### よくある問題と解決方法

1. **「Python が見つかりません」**
   - Python 3.8以上をインストール
   - Linux: `sudo apt install python3 python3-venv`
   - macOS: `brew install python3`
   - Windows: https://www.python.org/downloads/

2. **「権限エラー」**
   - Linux/macOS: `chmod +x setup_and_run.sh`
   - Windows: 管理者権限で実行

3. **「ポート使用中」**
   - 他のWebサーバーを停止
   - `lsof -ti:5000 | xargs kill -9` (Linux/macOS)
   - タスクマネージャーでプロセス終了 (Windows)

4. **「依存関係インストール失敗」**
   - インターネット接続確認
   - 社内プロキシ設定確認
   - `pip install --upgrade pip`

## 📞 サポート

社内でのセットアップに問題がある場合：
1. エラーメッセージを記録
2. 環境情報を収集（OS、Python版）
3. IT サポートに連絡

---

**Word Image Maker Ver.2** - 誰でも簡単に英単語イラスト生成！