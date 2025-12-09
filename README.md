# mimamori-pi

Raspberry Pi ベースの新生児見守りカメラシステム

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

