"""アプリケーション設定管理モジュール."""

import os
from pathlib import Path

from dotenv import load_dotenv


class Settings:
    """アプリケーション設定を管理するクラス.

    環境変数から設定を読み込み、デフォルト値を提供します。
    Flask設定とカメラ設定を含みます。
    """

    def __init__(self, env_file: str | Path | None = None) -> None:
        """Settingsインスタンスを初期化.

        Args:
            env_file: .envファイルのパス。Noneの場合は自動検出。
        """
        # 環境変数を読み込む
        if env_file is None:
            # プロジェクトルートを探す
            project_root = self._find_project_root()
            env_file = project_root / ".env"
        load_dotenv(env_file)

        # Flask基本設定
        self.HOST: str = self._get_env("FLASK_HOST", "0.0.0.0")
        self.PORT: int = self._get_env_int("FLASK_PORT", 5000)
        self.SECRET_KEY: str = self._get_env(
            "SECRET_KEY",
            "dev-secret-key-change-in-production",
        )
        self.DEBUG: bool = self._get_env_bool("FLASK_DEBUG", False)

        # カメラ基本設定
        self.CAMERA_RESOLUTION: tuple[int, int] = self._get_resolution()
        self.CAMERA_FRAMERATE: int = self._get_env_int("CAMERA_FRAMERATE", 15)

    def _find_project_root(self) -> Path:
        """プロジェクトルートディレクトリを検出.

        Returns:
            プロジェクトルートのPathオブジェクト。
        """
        current = Path(__file__).resolve()
        # src/mimamori_pi/config/settings.py から プロジェクトルートへ
        # 4階層上に移動
        for _ in range(4):
            current = current.parent
        return current

    def _get_env(self, key: str, default: str) -> str:
        """環境変数を取得（文字列）.

        Args:
            key: 環境変数名
            default: デフォルト値

        Returns:
            環境変数の値、存在しない場合はデフォルト値
        """
        return os.getenv(key, default)

    def _get_env_int(self, key: str, default: int) -> int:
        """環境変数を取得（整数）.

        Args:
            key: 環境変数名
            default: デフォルト値

        Returns:
            環境変数の値を整数に変換した値、存在しない場合はデフォルト値
        """
        value = os.getenv(key)
        if value is None:
            return default
        try:
            return int(value)
        except ValueError:
            return default

    def _get_env_bool(self, key: str, default: bool) -> bool:
        """環境変数を取得（真偽値）.

        Args:
            key: 環境変数名
            default: デフォルト値

        Returns:
            環境変数の値を真偽値に変換した値、存在しない場合はデフォルト値
        """
        value = os.getenv(key)
        if value is None:
            return default
        return value.lower() in ("true", "1", "yes", "on")

    def _get_resolution(self) -> tuple[int, int]:
        """カメラ解像度を取得.

        環境変数 CAMERA_RESOLUTION から "WIDTHxHEIGHT" 形式で読み込む。
        例: "640x480"

        Returns:
            (幅, 高さ) のタプル。デフォルトは (640, 480)
        """
        value = os.getenv("CAMERA_RESOLUTION", "640x480")
        try:
            width, height = value.split("x")
            return (int(width), int(height))
        except (ValueError, AttributeError):
            return (640, 480)

    def to_flask_config(self) -> dict[str, str | int | bool]:
        """Flask設定用の辞書を返す.

        Returns:
            Flaskアプリケーションに渡す設定辞書
        """
        return {
            "HOST": self.HOST,
            "PORT": self.PORT,
            "SECRET_KEY": self.SECRET_KEY,
            "DEBUG": self.DEBUG,
        }

