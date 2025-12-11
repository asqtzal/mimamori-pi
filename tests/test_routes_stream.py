"""ストリーミングルートのテスト."""

from collections.abc import Iterator
from unittest.mock import MagicMock, patch

import pytest

from mimamori_pi.app import app, camera_service


@pytest.fixture
def client():
    """Flaskテストクライアントを作成."""
    with app.test_client() as test_client:
        yield test_client


@pytest.fixture
def mock_camera_service_start():
    """CameraService.start()をモック化."""
    with patch.object(camera_service, "start") as mock_start:
        yield mock_start


@pytest.fixture
def mock_camera_service_stop():
    """CameraService.stop()をモック化."""
    with patch.object(camera_service, "stop") as mock_stop:
        yield mock_stop


@pytest.fixture
def mock_camera_service_generate_stream():
    """CameraService.generate_stream()をモック化."""
    with patch.object(camera_service, "generate_stream") as mock_stream:
        yield mock_stream


class TestVideoFeedRoute:
    """`/video_feed`ルートのテスト."""

    def test_video_feed_success(self, client, mock_camera_service_generate_stream):
        """正常系: Motion JPEGストリームが返されることを確認."""
        # モックストリームを設定（JPEGフレームを模擬）
        mock_frame = (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            b"\xff\xd8\xff\xe0\x00\x10JFIF"  # 簡易JPEGヘッダー
            b"\r\n"
        )

        def mock_stream_generator() -> Iterator[bytes]:
            yield mock_frame

        mock_camera_service_generate_stream.return_value = mock_stream_generator()

        # カメラが起動している状態をモック
        camera_service._camera = MagicMock()

        response = client.get("/video_feed")
        assert response.status_code == 200
        assert response.mimetype == "multipart/x-mixed-replace"
        # boundaryパラメータはContent-Typeヘッダーに含まれる
        assert "boundary=frame" in response.headers.get("Content-Type", "")
        assert b"--frame" in response.data

    def test_video_feed_camera_not_started(self, client, mock_camera_service_generate_stream):
        """カメラが起動していない場合、エラーが返されることを確認."""
        # カメラが起動していない状態をモック
        camera_service._camera = None

        # RuntimeErrorを発生させる
        mock_camera_service_generate_stream.side_effect = RuntimeError(
            "Camera is not started. Call start() before generate_stream()."
        )

        response = client.get("/video_feed")
        assert response.status_code == 500
        assert b"Camera error" in response.data

    def test_video_feed_picamera2_not_available(
        self, client, mock_camera_service_generate_stream
    ):
        """picamera2が利用できない場合、エラーが返されることを確認."""
        # picamera2未利用エラーを発生させる
        mock_camera_service_generate_stream.side_effect = RuntimeError(
            "picamera2 is not available. Please install picamera2 on Raspberry Pi."
        )

        response = client.get("/video_feed")
        assert response.status_code == 500
        assert b"Camera error" in response.data


class TestStreamStartRoute:
    """`/stream/start`ルートのテスト."""

    def test_stream_start_success(self, client, mock_camera_service_start):
        """正常系: ストリーミングが開始されることを確認."""
        mock_camera_service_start.return_value = None

        response = client.post("/stream/start")
        assert response.status_code == 200
        assert response.is_json
        data = response.get_json()
        assert data is not None
        assert data["status"] == "success"
        assert data["message"] == "Stream started"
        mock_camera_service_start.assert_called_once()

    def test_stream_start_failure(self, client, mock_camera_service_start):
        """エラー系: カメラ起動に失敗した場合、エラーが返されることを確認."""
        mock_camera_service_start.side_effect = RuntimeError("Camera initialization failed")

        response = client.post("/stream/start")
        assert response.status_code == 500
        assert response.is_json
        data = response.get_json()
        assert data is not None
        assert data["status"] == "error"
        assert "Camera initialization failed" in data["message"]


class TestStreamStopRoute:
    """`/stream/stop`ルートのテスト."""

    def test_stream_stop_success(self, client, mock_camera_service_stop):
        """正常系: ストリーミングが停止されることを確認."""
        mock_camera_service_stop.return_value = None

        response = client.post("/stream/stop")
        assert response.status_code == 200
        assert response.is_json
        data = response.get_json()
        assert data is not None
        assert data["status"] == "success"
        assert data["message"] == "Stream stopped"
        mock_camera_service_stop.assert_called_once()

    def test_stream_stop_failure(self, client, mock_camera_service_stop):
        """エラー系: カメラ停止に失敗した場合、エラーが返されることを確認."""
        mock_camera_service_stop.side_effect = Exception("Stop failed")

        response = client.post("/stream/stop")
        assert response.status_code == 500
        assert response.is_json
        data = response.get_json()
        assert data is not None
        assert data["status"] == "error"
        assert "Stop failed" in data["message"]

    def test_stream_stop_get_method_not_allowed(self, client):
        """GETメソッドは許可されていないことを確認."""
        response = client.get("/stream/stop")
        assert response.status_code == 405  # Method Not Allowed


class TestStreamStartStopIntegration:
    """ストリーミング開始・停止の統合テスト."""

    def test_start_then_stop(self, client, mock_camera_service_start, mock_camera_service_stop):
        """開始→停止の順序で動作することを確認."""
        # 開始
        response = client.post("/stream/start")
        assert response.status_code == 200

        # 停止
        response = client.post("/stream/stop")
        assert response.status_code == 200

        # 各メソッドが1回ずつ呼ばれたことを確認
        mock_camera_service_start.assert_called_once()
        mock_camera_service_stop.assert_called_once()

