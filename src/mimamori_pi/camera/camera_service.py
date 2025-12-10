"""カメラ制御サービスモジュール."""

import logging

try:
    from picamera2 import Picamera2
except ImportError:
    Picamera2 = None

from mimamori_pi.config.settings import Settings

logger = logging.getLogger(__name__)


class CameraService:
    """カメラ制御を管理するクラス.

    picamera2を使用してカメラの起動・停止を制御します。
    将来的にはストリーミング、スナップショット取得などの機能を追加します。
    """

    def __init__(self, settings: Settings) -> None:
        """CameraServiceインスタンスを初期化.

        Args:
            settings: アプリケーション設定オブジェクト
        """
        self._settings = settings
        self._camera: Picamera2 | None = None

    def start(self) -> None:
        """カメラを起動する.

        カメラを初期化し、ストリーミング可能な状態にします。

        Raises:
            RuntimeError: picamera2が利用できない場合、またはカメラの初期化に失敗した場合
        """
        if Picamera2 is None:
            error_msg = "picamera2 is not available. Please install picamera2 on Raspberry Pi."
            logger.error(error_msg)
            raise RuntimeError(error_msg)

        if self._camera is not None:
            logger.warning("Camera is already started")
            return

        try:
            logger.info("Initializing camera...")
            self._camera = Picamera2()

            # カメラ設定を適用
            resolution = self._settings.CAMERA_RESOLUTION
            framerate = self._settings.CAMERA_FRAMERATE

            # プレビュー設定を作成（解像度とフレームレートを指定）
            camera_config = self._camera.create_preview_configuration(
                main={"size": resolution},
            )
            self._camera.configure(camera_config)

            # フレームレートを設定
            self._camera.set_controls({"FrameRate": framerate})

            # カメラを起動
            self._camera.start()
            logger.info(
                f"Camera started with resolution {resolution} and framerate {framerate}fps"
            )
        except Exception as e:
            logger.error(f"Failed to start camera: {e}", exc_info=True)
            self._camera = None
            raise RuntimeError(f"Failed to start camera: {e}") from e

    def stop(self) -> None:
        """カメラを停止する.

        カメラリソースを解放し、クリーンアップします。
        """
        if self._camera is None:
            logger.debug("Camera is not started")
            return

        try:
            logger.info("Stopping camera...")
            self._camera.stop()
            self._camera = None
            logger.info("Camera stopped")
        except Exception as e:
            logger.error(f"Error while stopping camera: {e}", exc_info=True)
            self._camera = None

