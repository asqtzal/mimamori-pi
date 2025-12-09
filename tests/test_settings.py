"""設定クラスのテスト."""

import os
from pathlib import Path
from unittest.mock import patch

from mimamori_pi.config.settings import Settings


class TestSettings:
    """Settingsクラスのテスト."""

    def test_default_values(self) -> None:
        """デフォルト値が正しく設定されることを確認."""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            assert settings.HOST == "0.0.0.0"
            assert settings.PORT == 5000
            assert settings.SECRET_KEY == "dev-secret-key-change-in-production"
            assert settings.DEBUG is False
            assert settings.CAMERA_RESOLUTION == (640, 480)
            assert settings.CAMERA_FRAMERATE == 15

    def test_flask_host_from_env(self) -> None:
        """環境変数からFlask HOSTを読み込む."""
        with patch.dict(os.environ, {"FLASK_HOST": "127.0.0.1"}, clear=False):
            settings = Settings()
            assert settings.HOST == "127.0.0.1"

    def test_flask_port_from_env(self) -> None:
        """環境変数からFlask PORTを読み込む."""
        with patch.dict(os.environ, {"FLASK_PORT": "8080"}, clear=False):
            settings = Settings()
            assert settings.PORT == 8080

    def test_flask_port_invalid(self) -> None:
        """無効なPORT値はデフォルト値を使用."""
        with patch.dict(os.environ, {"FLASK_PORT": "invalid"}, clear=False):
            settings = Settings()
            assert settings.PORT == 5000

    def test_secret_key_from_env(self) -> None:
        """環境変数からSECRET_KEYを読み込む."""
        with patch.dict(
            os.environ,
            {"SECRET_KEY": "production-secret-key"},
            clear=False,
        ):
            settings = Settings()
            assert settings.SECRET_KEY == "production-secret-key"

    def test_debug_from_env(self) -> None:
        """環境変数からDEBUGを読み込む."""
        test_cases = [
            ("true", True),
            ("True", True),
            ("1", True),
            ("yes", True),
            ("on", True),
            ("false", False),
            ("False", False),
            ("0", False),
            ("no", False),
            ("off", False),
        ]
        for env_value, expected in test_cases:
            with patch.dict(os.environ, {"FLASK_DEBUG": env_value}, clear=False):
                settings = Settings()
                assert expected == settings.DEBUG, f"Failed for {env_value}"

    def test_camera_resolution_from_env(self) -> None:
        """環境変数からカメラ解像度を読み込む."""
        with patch.dict(os.environ, {"CAMERA_RESOLUTION": "1280x720"}, clear=False):
            settings = Settings()
            assert settings.CAMERA_RESOLUTION == (1280, 720)

    def test_camera_resolution_default(self) -> None:
        """カメラ解像度のデフォルト値を確認."""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            assert settings.CAMERA_RESOLUTION == (640, 480)

    def test_camera_resolution_invalid(self) -> None:
        """無効な解像度値はデフォルト値を使用."""
        test_cases = ["invalid", "640", "640x", "x480", "abcxdef"]
        for invalid_value in test_cases:
            with patch.dict(
                os.environ,
                {"CAMERA_RESOLUTION": invalid_value},
                clear=False,
            ):
                settings = Settings()
                assert settings.CAMERA_RESOLUTION == (640, 480)

    def test_camera_framerate_from_env(self) -> None:
        """環境変数からカメラフレームレートを読み込む."""
        with patch.dict(os.environ, {"CAMERA_FRAMERATE": "30"}, clear=False):
            settings = Settings()
            assert settings.CAMERA_FRAMERATE == 30

    def test_camera_framerate_invalid(self) -> None:
        """無効なフレームレート値はデフォルト値を使用."""
        with patch.dict(os.environ, {"CAMERA_FRAMERATE": "invalid"}, clear=False):
            settings = Settings()
            assert settings.CAMERA_FRAMERATE == 15

    def test_to_flask_config(self) -> None:
        """Flask設定辞書が正しく生成されることを確認."""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            config = settings.to_flask_config()
            assert config["HOST"] == "0.0.0.0"
            assert config["PORT"] == 5000
            assert config["SECRET_KEY"] == "dev-secret-key-change-in-production"
            assert config["DEBUG"] is False

    def test_custom_env_file(self, tmp_path: Path) -> None:
        """カスタム.envファイルから設定を読み込む."""
        env_file = tmp_path / ".env"
        env_file.write_text("FLASK_HOST=192.168.1.100\nFLASK_PORT=9000\n")
        settings = Settings(env_file=env_file)
        assert settings.HOST == "192.168.1.100"
        assert settings.PORT == 9000

