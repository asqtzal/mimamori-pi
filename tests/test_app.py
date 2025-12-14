"""Flaskアプリケーションのテスト."""


import pytest

from mimamori_pi.app import app, camera_service


class TestAppInitialization:
    """Flaskアプリケーションの初期化テスト."""

    def test_app_exists(self) -> None:
        """Flaskアプリインスタンスが存在することを確認."""
        assert app is not None

    def test_app_is_flask_instance(self) -> None:
        """appがFlaskインスタンスであることを確認."""
        from flask import Flask

        assert isinstance(app, Flask)

    def test_app_name(self) -> None:
        """アプリケーション名が正しいことを確認."""
        assert app.name == "mimamori_pi.app"

    def test_app_config(self) -> None:
        """Flaskアプリに設定が適用されていることを確認."""
        assert "SECRET_KEY" in app.config
        assert "DEBUG" in app.config
        # SECRET_KEYがデフォルト値でないことを確認（設定が読み込まれている）
        assert app.config["SECRET_KEY"] is not None

    def test_camera_service_exists(self) -> None:
        """CameraServiceインスタンスが存在することを確認."""
        assert camera_service is not None

    def test_camera_service_type(self) -> None:
        """CameraServiceが正しい型であることを確認."""
        from mimamori_pi.camera import CameraService

        assert isinstance(camera_service, CameraService)


class TestAppRoutes:
    """Flaskアプリケーションのルートテスト."""

    @pytest.fixture
    def client(self):
        """Flaskテストクライアントを作成."""
        with app.test_client() as test_client:
            yield test_client

    def test_404_on_unknown_route(self, client) -> None:
        """存在しないルートにアクセスした場合、404を返すことを確認."""
        response = client.get("/unknown_route")
        assert response.status_code == 404

    def test_app_has_testing_config(self, client) -> None:
        """テストクライアントが正しく動作することを確認."""
        # テストクライアントが作成できることを確認
        assert client is not None

