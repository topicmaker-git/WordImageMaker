# Word Image Maker Ver.2 - セットアップガイド

## 🚀 初心者向け簡単セットアップ

### Linux / macOS 用
```bash
# 1. プロジェクトをクローン
git clone https://github.com/topicmaker-git/WordImageMaker.git
cd WordImageMaker

# 2. 一括セットアップ・起動
./setup_and_run.sh
```

### Windows 用
```cmd
# 1. プロジェクトをクローン
git clone https://github.com/topicmaker-git/WordImageMaker.git
cd WordImageMaker

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

## 🎨 Webアプリの使い方

### 基本的な使い方

1. **API Key の設定**
   - 初回アクセス時に OpenAI API Key を入力
   - 👁️ボタンで表示/非表示を切り替え
   - ✏️ボタンで別のキーに変更可能
   - 🗑️ボタンで保存されたキーを削除

2. **英単語の入力**
   ```
   hello
   world
   bank#金融機関
   apple#果物
   ```
   - **複数単語**: 改行区切りで入力
   - **補足情報**: `単語#意味や品詞` で曖昧さを解消
   - **例**: `bank#金融機関` と `bank#土手` で区別

3. **詳細設定（オプション）**
   - **品質設定**: Auto（推奨）/ High / Medium / Low
   - **キャラクター画像**: デフォルトは `cat_and_mouse.png`
   - **キャラクター説明**: デフォルトは「仲の良い猫とねずみ」

### 生成プロセス

1. **「イラスト生成開始」ボタンをクリック**
2. **リアルタイム進捗表示**
   - 各単語の処理状況を表示
   - 成功・失敗をリアルタイムで確認
3. **結果の確認**
   - 生成されたイラストとコスト表示
   - 「表示」ボタンで詳細HTMLページを確認

## 📁 生成ファイルの保存場所

### ファイル構成
```
WordImageMaker/
├── output/                    # 生成結果保存フォルダ
│   ├── images/               # 生成画像（PNG形式）
│   │   ├── hello_20250711_123456.png
│   │   ├── world_20250711_123501.png
│   │   └── bank_20250711_123507.png
│   └── [単語]_viewer.html    # 確認用HTMLファイル
│       ├── hello_viewer.html
│       ├── world_viewer.html
│       └── bank_viewer.html
```

### 生成ファイルの詳細

#### 1. 画像ファイル（PNG形式）
- **保存場所**: `output/images/`
- **ファイル名**: `[単語]_[日付時刻].png`
- **例**: `hello_20250711_123456.png`
- **サイズ**: 1024×1024px
- **形式**: PNG（高品質）

#### 2. HTMLビューアファイル
- **保存場所**: `output/`
- **ファイル名**: `[単語]_viewer.html`
- **内容**: 
  - 生成された画像の表示
  - シーン説明とコアイメージ
  - 生成プロンプト
  - コスト情報

### ファイルの利用方法

#### 画像ファイルの直接利用
```bash
# 画像ファイルの場所
ls output/images/

# 他のアプリケーションで開く
open output/images/hello_20250711_123456.png  # macOS
xdg-open output/images/hello_20250711_123456.png  # Linux
```

#### HTMLファイルの確認
- ブラウザで直接開く
- 右パネルの「表示」ボタンをクリック
- ファイルシステムから直接開く

## 🖼️ キャラクター画像のカスタマイズ

### デフォルトキャラクター
プロジェクトには以下が含まれています：
```
image/
├── cat_and_mouse.jpeg    # 元画像（JPEG）
└── cat_and_mouse.png     # PNG変換版（使用推奨）
```

### カスタムキャラクターの追加

1. **画像ファイルの準備**
   ```bash
   # PNG形式（推奨）でimage/フォルダに配置
   image/
   ├── cat_and_mouse.png     # デフォルト
   ├── my_character.png      # カスタム画像
   └── school_kids.png       # 例：学校の子供たち
   ```

2. **Webアプリでの設定**
   - 詳細設定を開く
   - 「キャラクター画像」に `my_character.png` を入力
   - 「キャラクター説明」に適切な説明を入力

### 推奨画像仕様
- **形式**: PNG（透明背景推奨）
- **サイズ**: 1024x1024px（正方形）
- **内容**: 表情豊かなキャラクター
- **背景**: シンプルまたは透明

## 💡 効果的な使い方のコツ

### 1. 単語の補足情報の活用
```
# 同じスペルで意味が異なる単語
bank#金融機関
bank#川の土手

# 品詞を明確にする
run#動詞、走る
run#名詞、実行

# 特定の文脈を指定
light#明るい（形容詞）
light#軽い（重量）
```

### 2. バッチ処理の活用
- 関連する単語をまとめて処理
- コスト効率が良い
- 一貫したスタイルで生成

### 3. 品質設定の使い分け
- **Auto**: 通常使用（推奨）
- **High**: 重要な単語、プレゼン用
- **Medium**: 練習用、確認用
- **Low**: テスト用、コスト重視

## 📊 コスト管理

- **1単語あたり**: 約$0.04-0.05（4-5円）
- **リアルタイム表示**: 生成前後にコスト確認
- **総コスト**: バッチ処理時の合計表示
- **詳細内訳**: 各単語の個別コスト表示

### 生成済みファイルの管理

- **右パネル**: 過去の生成結果を一覧表示
- **🔄 更新ボタン**: 最新の生成結果を取得
- **👁️ 表示ボタン**: 各単語の詳細ページを表示
- **直接アクセス**: `output/` フォルダから直接ファイルを利用可能

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