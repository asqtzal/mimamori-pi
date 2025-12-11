"""Flaskアプリケーションエントリーポイント."""

from flask import Flask

from mimamori_pi.camera import CameraService
from mimamori_pi.config import Settings, setup_logging

# ロギング設定を初期化（最初に実行）
setup_logging()

# アプリケーション設定を読み込み
settings = Settings()

# Flaskアプリインスタンスを作成
app = Flask(__name__)

# Flaskアプリに設定を適用
app.config.update(settings.to_flask_config())

# CameraServiceインスタンスを作成
camera_service = CameraService(settings)

# ルートを登録
from mimamori_pi.routes import stream  # noqa: F401, E402

if __name__ == "__main__":
    # アプリケーションを起動
    app.run(
        host=settings.HOST,
        port=settings.PORT,
        debug=settings.DEBUG,
    )

