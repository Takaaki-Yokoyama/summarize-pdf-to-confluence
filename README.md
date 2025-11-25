# summarize-pdf-to-confluence

PDFファイルを読み込んで、Google Gemini AIで要約し、要約内容をConfluenceのページにアップロードするPythonツール。

## 機能

- PDFファイルからテキストを抽出
- Google Gemini AIを使用してテキストを日本語で要約
- 要約結果をConfluenceページとして自動作成/更新

## 必要条件

- Python 3.10以上
- Google Gemini API Key
- Confluence API Token

## インストール

```bash
# リポジトリをクローン
git clone https://github.com/Takaaki-Yokoyama/summarize-pdf-to-confluence.git
cd summarize-pdf-to-confluence

# 依存関係をインストール
pip install -r requirements.txt
```

## 設定

1. `.env.example`を`.env`にコピーして、必要な情報を設定します：

```bash
cp .env.example .env
```

2. `.env`ファイルを編集して、以下の情報を設定します：

```
# Google Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here

# Confluence settings
CONFLUENCE_URL=https://your-domain.atlassian.net/wiki
CONFLUENCE_USERNAME=your_email@example.com
CONFLUENCE_API_TOKEN=your_confluence_api_token_here
CONFLUENCE_SPACE_KEY=YOUR_SPACE_KEY
```

### API Keyの取得方法

#### Gemini API Key
1. [Google AI Studio](https://aistudio.google.com/apikey)にアクセス
2. 「Get API Key」をクリックしてAPIキーを取得

#### Confluence API Token
1. [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens)にアクセス
2. 「Create API token」をクリックしてトークンを作成

## 使い方

### 基本的な使い方

```bash
python main.py path/to/document.pdf
```

### オプション

```bash
# カスタムタイトルを指定
python main.py document.pdf --title "カスタムページタイトル"

# 親ページを指定
python main.py document.pdf --parent-id 12345678

# すべてのオプションを使用
python main.py document.pdf --title "要約ページ" --parent-id 12345678
```

### コマンドラインオプション

| オプション | 短縮形 | 説明 |
|-----------|--------|------|
| `--title` | `-t` | Confluenceページのタイトル（デフォルト: "PDF要約: ファイル名"） |
| `--parent-id` | `-p` | 親ページのID（階層構造を作成する場合） |

## プロジェクト構成

```
summarize-pdf-to-confluence/
├── main.py                 # メインエントリーポイント
├── requirements.txt        # 依存関係
├── .env.example           # 環境変数テンプレート
├── .gitignore             # Git除外ファイル
├── README.md              # このファイル
└── src/
    ├── __init__.py
    ├── config.py          # 設定読み込み
    ├── pdf_reader.py      # PDF読み取り
    ├── gemini_client.py   # Gemini API連携
    └── confluence_client.py # Confluence API連携
```

## ライセンス

MIT License
