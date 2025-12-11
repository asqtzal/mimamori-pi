"""カメラサービスのテスト."""

from unittest.mock import MagicMock, patch

import pytest

from mimamori_pi.camera.camera_service import CameraService
from mimamori_pi.config.settings import Settings


@pytest.fixture
def mock_settings() -> Settings:
    """Settingsモックを作成."""
    settings = Settings()
    settings.CAMERA_RESOLUTION = (640, 480)
    settings.CAMERA_FRAMERATE = 15
    return settings


@pytest.fixture
def mock_picamera2() -> MagicMock:
    """Picamera2モックを作成."""
    mock_camera = MagicMock()
    mock_config = MagicMock()
    mock_camera.create_preview_configuration.return_value = mock_config
    return mock_camera


class TestCameraService:
    """CameraServiceクラスのテスト."""

    def test_init(self, mock_settings: Settings) -> None:
        """__init__メソッドが正しく動作することを確認."""
        service = CameraService(mock_settings)
        assert service._settings == mock_settings
        assert service._camera is None

    @patch("mimamori_pi.camera.camera_service.Picamera2", None)
    def test_start_without_picamera2(self, mock_settings: Settings) -> None:
        """picamera2が利用できない場合にRuntimeErrorが発生することを確認."""
        service = CameraService(mock_settings)
        with pytest.raises(RuntimeError, match="picamera2 is not available"):
            service.start()

    @patch("mimamori_pi.camera.camera_service.Picamera2")
    def test_start_success(
        self,
        mock_picamera2_class: MagicMock,
        mock_settings: Settings,
        mock_picamera2: MagicMock,
    ) -> None:
        """startメソッドが正常に動作することを確認."""
        mock_picamera2_class.return_value = mock_picamera2

        service = CameraService(mock_settings)
        service.start()

        # Picamera2が作成されたことを確認
        mock_picamera2_class.assert_called_once()
        # 設定が適用されたことを確認
        mock_picamera2.create_preview_configuration.assert_called_once_with(
            main={"size": (640, 480)}
        )
        mock_picamera2.configure.assert_called_once()
        mock_picamera2.set_controls.assert_called_once_with({"FrameRate": 15})
        # カメラが起動されたことを確認
        mock_picamera2.start.assert_called_once()
        # カメラインスタンスが保存されたことを確認
        assert service._camera == mock_picamera2

    @patch("mimamori_pi.camera.camera_service.Picamera2")
    def test_start_already_started(
        self,
        mock_picamera2_class: MagicMock,
        mock_settings: Settings,
        mock_picamera2: MagicMock,
    ) -> None:
        """既に起動中のカメラに対してstartを呼び出してもエラーにならないことを確認."""
        mock_picamera2_class.return_value = mock_picamera2

        service = CameraService(mock_settings)
        service.start()
        # 2回目のstart呼び出し
        service.start()

        # Picamera2は1回だけ作成されることを確認
        assert mock_picamera2_class.call_count == 1

    @patch("mimamori_pi.camera.camera_service.Picamera2")
    def test_start_initialization_error(
        self,
        mock_picamera2_class: MagicMock,
        mock_settings: Settings,
    ) -> None:
        """カメラ初期化時にエラーが発生した場合にRuntimeErrorが発生することを確認."""
        mock_picamera2_class.side_effect = Exception("Camera initialization failed")

        service = CameraService(mock_settings)
        with pytest.raises(RuntimeError, match="Failed to start camera"):
            service.start()

        # エラー後、カメラインスタンスがNoneにリセットされることを確認
        assert service._camera is None

    @patch("mimamori_pi.camera.camera_service.Picamera2")
    def test_stop_success(
        self,
        mock_picamera2_class: MagicMock,
        mock_settings: Settings,
        mock_picamera2: MagicMock,
    ) -> None:
        """stopメソッドが正常に動作することを確認."""
        mock_picamera2_class.return_value = mock_picamera2

        service = CameraService(mock_settings)
        service.start()
        service.stop()

        # カメラが停止されたことを確認
        mock_picamera2.stop.assert_called_once()
        # カメラインスタンスがNoneにリセットされたことを確認
        assert service._camera is None

    def test_stop_not_started(self, mock_settings: Settings) -> None:
        """カメラが起動していない状態でstopを呼び出してもエラーにならないことを確認."""
        service = CameraService(mock_settings)
        # エラーが発生しないことを確認
        service.stop()
        assert service._camera is None

    @patch("mimamori_pi.camera.camera_service.Picamera2")
    def test_stop_error_handling(
        self,
        mock_picamera2_class: MagicMock,
        mock_settings: Settings,
        mock_picamera2: MagicMock,
    ) -> None:
        """stopメソッドでエラーが発生した場合でもカメラインスタンスがリセットされることを確認."""
        mock_picamera2_class.return_value = mock_picamera2
        mock_picamera2.stop.side_effect = Exception("Stop error")

        service = CameraService(mock_settings)
        service.start()
        service.stop()

        # エラー後でもカメラインスタンスがNoneにリセットされることを確認
        assert service._camera is None

    @patch("mimamori_pi.camera.camera_service.Picamera2")
    def test_generate_stream_success(
        self,
        mock_picamera2_class: MagicMock,
        mock_settings: Settings,
        mock_picamera2: MagicMock,
    ) -> None:
        """generate_streamがMJPEGフレームを返すことを確認."""
        mock_picamera2_class.return_value = mock_picamera2

        # capture_fileがBytesIOへダミーJPEGを書き込むように設定
        def fake_capture(buffer: MagicMock, format: str = "jpeg") -> None:
            buffer.write(b"jpegdata")

        mock_picamera2.capture_file.side_effect = fake_capture

        service = CameraService(mock_settings)
        service._camera = mock_picamera2  # startをモックする代わりに直接セット

        stream = service.generate_stream()
        frame = next(stream)

        assert frame.startswith(b"--frame\r\nContent-Type: image/jpeg\r\n\r\njpegdata")
        assert frame.endswith(b"\r\n")

    @patch("mimamori_pi.camera.camera_service.Picamera2")
    def test_generate_stream_without_camera(
        self, mock_picamera2_class: MagicMock, mock_settings: Settings
    ) -> None:
        """カメラ未起動でgenerate_streamを呼ぶとRuntimeErrorになることを確認."""
        service = CameraService(mock_settings)
        with pytest.raises(RuntimeError, match="Camera is not started"):
            service.generate_stream()

    @patch("mimamori_pi.camera.camera_service.Picamera2", None)
    def test_generate_stream_without_picamera2(self, mock_settings: Settings) -> None:
        """picamera2未インストール時はRuntimeErrorになることを確認."""
        service = CameraService(mock_settings)
        with pytest.raises(RuntimeError, match="picamera2 is not available"):
            service.generate_stream()

    @patch("mimamori_pi.camera.camera_service.Picamera2")
    def test_generate_stream_capture_error(
        self,
        mock_picamera2_class: MagicMock,
        mock_settings: Settings,
        mock_picamera2: MagicMock,
    ) -> None:
        """フレーム生成中の例外がRuntimeErrorにラップされることを確認."""
        mock_picamera2_class.return_value = mock_picamera2
        mock_picamera2.capture_file.side_effect = Exception("capture failed")

        service = CameraService(mock_settings)
        service._camera = mock_picamera2

        stream = service.generate_stream()
        with pytest.raises(RuntimeError, match="Failed to generate stream"):
            next(stream)

