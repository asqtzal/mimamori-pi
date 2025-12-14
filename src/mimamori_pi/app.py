"""Flaskアプリケーションエントリーポイント."""

from flask import Flask

from mimamori_pi.camera import CameraService
from mimamori_pi.config import Settings, setup_logging
from mimamori_pi.routes.main import bp as main_bp
from mimamori_pi.routes.stream import bp as stream_bp

# ロギング設定を初期化（最初に実行）
setup_logging()

# アプリケーション設定を読み込み
settings = Settings()

# Flaskアプリインスタンスを作成
app = Flask(__name__)

app.register_blueprint(main_bp)
app.register_blueprint(stream_bp)
# Flaskアプリに設定を適用
app.config.update(settings.to_flask_config())

# CameraServiceインスタンスを作成
camera_service = CameraService(settings)

if __name__ == "__main__":
    # アプリケーションを起動
    app.run(
        host=settings.HOST,
        port=settings.PORT,
        debug=settings.DEBUG,
    )

