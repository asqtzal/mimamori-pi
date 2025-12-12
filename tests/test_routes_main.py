"""メインルートのテスト."""

import pytest

from mimamori_pi.app import app


@pytest.fixture
def client():
    """Flaskテストクライアントを作成."""
    with app.test_client() as test_client:
        yield test_client


class TestMainRoute:
    """`/`ルートのテスト."""

    def test_index_renders_template(self, client):
        """正常系: index.htmlが正しくレンダリングされることを確認."""
        response = client.get("/")
        assert response.status_code == 200
        assert response.mimetype == "text/html"

    def test_index_contains_title(self, client):
        """index.htmlにタイトルが含まれていることを確認."""
        response = client.get("/")
        assert response.status_code == 200
        # HTMLにタイトルが含まれていることを確認
        assert b"mimamori-pi" in response.data

    def test_index_contains_video_stream(self, client):
        """index.htmlにビデオストリームのimgタグが含まれていることを確認."""
        response = client.get("/")
        assert response.status_code == 200
        # video_feedへの参照が含まれていることを確認
        assert b"/video_feed" in response.data
        assert b'<img' in response.data or b'<IMG' in response.data

    def test_index_contains_start_button(self, client):
        """index.htmlに開始ボタンが含まれていることを確認."""
        response = client.get("/")
        assert response.status_code == 200
        # 開始ボタンが含まれていることを確認
        assert "ストリーム開始".encode() in response.data
        assert b'id="start-btn"' in response.data or b'id=\'start-btn\'' in response.data

    def test_index_contains_stop_button(self, client):
        """index.htmlに停止ボタンが含まれていることを確認."""
        response = client.get("/")
        assert response.status_code == 200
        # 停止ボタンが含まれていることを確認
        assert "ストリーム停止".encode() in response.data
        assert b'id="stop-btn"' in response.data or b'id=\'stop-btn\'' in response.data

    def test_index_contains_javascript(self, client):
        """index.htmlにJavaScriptが含まれていることを確認."""
        response = client.get("/")
        assert response.status_code == 200
        # JavaScriptのfetch呼び出しが含まれていることを確認
        assert b"/stream/start" in response.data
        assert b"/stream/stop" in response.data
        assert b"fetch" in response.data or b"Fetch" in response.data

    def test_index_extends_base_template(self, client):
        """index.htmlがbase.htmlを継承していることを確認."""
        response = client.get("/")
        assert response.status_code == 200
        # base.htmlの基本構造が含まれていることを確認
        assert b"<!DOCTYPE html>" in response.data
        assert b'<html' in response.data or b'<HTML' in response.data
        assert b'lang="ja"' in response.data or b"lang='ja'" in response.data

