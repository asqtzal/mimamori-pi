# mimamori-pi

Raspberry Pi ベースの新生児見守りカメラシステム

## 概要

mimamori-piは、Raspberry Pi上で動作するPython/Flaskベースの赤ちゃん見守りシステムです。picamera2ライブラリを使用してカメラを制御し、Motion JPEG形式でリアルタイムストリーミングを提供します。


## セットアップ

### Mac / 開発

```bash
uv sync --group dev
```

### Raspberry Pi 本番

```bash
uv sync -p pyproject.pi.toml
```

## 設定

アプリケーション設定は環境変数または `.env` ファイルで管理します。

### 環境変数の設定

プロジェクトルートに `.env` ファイルを作成し、以下の環境変数を設定できます：

```bash
# Flask設定
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
SECRET_KEY=your-secret-key-here
FLASK_DEBUG=false

# カメラ設定
CAMERA_RESOLUTION=640x480
CAMERA_FRAMERATE=15

# ログ設定
MIMAMORI_PI_LOG_LEVEL=INFO
```

各設定項目の詳細は `.kiro/steering/build_and_test.md` を参照してください。

## ログ

ログは以下の場所に出力されます：
- コンソール: 標準エラー出力
- ファイル: `data/logs/mimamori-pi.log`（自動的に作成されます）

ログレベルは環境変数 `MIMAMORI_PI_LOG_LEVEL` で制御できます（`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`）。

**注意**: `.env` ファイルには秘匿情報を含むため、Gitにコミットしないでください。

## 起動方法

### 開発環境での起動

```bash
# 依存関係のインストール
uv sync --group dev

# アプリケーションの起動
uv run python -m mimamori_pi.app
```

ブラウザで `http://localhost:5000` にアクセスしてください。

### 利用可能なエンドポイント

- `GET /`: メインページ（index.html）
- `GET /video_feed`: Motion JPEGストリーム（カメラ起動後）
- `POST /stream/start`: ストリーミング開始
- `POST /stream/stop`: ストリーミング停止

## テスト

```bash
# 全テスト実行
uv run pytest

# 特定のテストファイル実行
uv run pytest tests/test_routes_stream.py

# カバレッジレポート付き
uv run pytest --cov
```

## コード品質チェック

```bash
# フォーマット
uv run ruff format .

# リント
uv run ruff check .

# 型チェック
uv run mypy src/
```

