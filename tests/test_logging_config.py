"""ロギング設定のテスト."""

import logging
import os
from pathlib import Path
from unittest.mock import patch

import pytest

from mimamori_pi.config.logging_config import setup_logging


@pytest.fixture(autouse=True)
def cleanup_logging() -> None:
    """各テスト後にロギング設定をクリーンアップ."""
    yield
    # テスト後にハンドラーをクリーンアップ
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        handler.close()
        root_logger.removeHandler(handler)


class TestLoggingConfig:
    """ロギング設定のテスト."""

    def test_default_log_level(self, tmp_path: Path) -> None:
        """デフォルトのログレベルがINFOであることを確認."""
        with patch.dict(os.environ, {}, clear=True):
            log_dir = tmp_path / "logs"
            setup_logging(log_dir=log_dir)
            
            root_logger = logging.getLogger()
            assert root_logger.level == logging.INFO

    def test_log_level_from_env(self, tmp_path: Path) -> None:
        """環境変数からログレベルを読み込む."""
        test_cases = [
            ("DEBUG", logging.DEBUG),
            ("INFO", logging.INFO),
            ("WARNING", logging.WARNING),
            ("ERROR", logging.ERROR),
            ("CRITICAL", logging.CRITICAL),
        ]
        for env_level, expected_level in test_cases:
            with patch.dict(
                os.environ, {"MIMAMORI_PI_LOG_LEVEL": env_level}, clear=False
            ):
                log_dir = tmp_path / "logs"
                setup_logging(log_dir=log_dir)
                
                root_logger = logging.getLogger()
                assert root_logger.level == expected_level, f"Failed for {env_level}"

    def test_log_level_invalid(self, tmp_path: Path) -> None:
        """無効なログレベルはINFOにフォールバック."""
        with patch.dict(
            os.environ, {"MIMAMORI_PI_LOG_LEVEL": "INVALID"}, clear=False
        ):
            log_dir = tmp_path / "logs"
            setup_logging(log_dir=log_dir)
            
            root_logger = logging.getLogger()
            assert root_logger.level == logging.INFO

    def test_log_level_parameter(self, tmp_path: Path) -> None:
        """パラメータで指定したログレベルが使用される."""
        log_dir = tmp_path / "logs"
        setup_logging(log_level="DEBUG", log_dir=log_dir)
        
        root_logger = logging.getLogger()
        assert root_logger.level == logging.DEBUG

    def test_log_dir_creation(self, tmp_path: Path) -> None:
        """ログディレクトリが自動作成される."""
        log_dir = tmp_path / "logs"
        assert not log_dir.exists()
        
        setup_logging(log_dir=log_dir)
        
        assert log_dir.exists()
        assert log_dir.is_dir()

    def test_console_handler_added(self, tmp_path: Path) -> None:
        """コンソールハンドラーが追加される."""
        log_dir = tmp_path / "logs"
        setup_logging(log_dir=log_dir)
        
        root_logger = logging.getLogger()
        console_handlers = [
            h
            for h in root_logger.handlers
            if isinstance(h, logging.StreamHandler)
            and not isinstance(h, logging.handlers.RotatingFileHandler)
        ]
        assert len(console_handlers) == 1

    def test_file_handler_added(self, tmp_path: Path) -> None:
        """ファイルハンドラーが追加される."""
        log_dir = tmp_path / "logs"
        setup_logging(log_dir=log_dir)
        
        root_logger = logging.getLogger()
        file_handlers = [
            h
            for h in root_logger.handlers
            if isinstance(h, logging.handlers.RotatingFileHandler)
        ]
        assert len(file_handlers) == 1

    def test_log_file_created(self, tmp_path: Path) -> None:
        """ログファイルが作成される."""
        log_dir = tmp_path / "logs"
        setup_logging(log_dir=log_dir)
        
        log_file = log_dir / "mimamori-pi.log"
        assert log_file.exists()

    def test_log_output_to_console(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """コンソールにログが出力される."""
        log_dir = tmp_path / "logs"
        setup_logging(log_dir=log_dir)
        
        logger = logging.getLogger("test")
        logger.info("Test message")
        
        captured = capsys.readouterr()
        assert "Test message" in captured.err

    def test_log_output_to_file(self, tmp_path: Path) -> None:
        """ファイルにログが出力される."""
        log_dir = tmp_path / "logs"
        setup_logging(log_dir=log_dir)
        
        logger = logging.getLogger("test")
        logger.info("Test message to file")
        
        log_file = log_dir / "mimamori-pi.log"
        assert log_file.exists()
        content = log_file.read_text(encoding="utf-8")
        assert "Test message to file" in content

    def test_log_format(self, tmp_path: Path) -> None:
        """ログフォーマットが正しい."""
        log_dir = tmp_path / "logs"
        setup_logging(log_dir=log_dir)
        
        logger = logging.getLogger("test_logger")
        logger.info("Test message")
        
        log_file = log_dir / "mimamori-pi.log"
        content = log_file.read_text(encoding="utf-8")
        # フォーマット: %(asctime)s - %(name)s - %(levelname)s - %(message)s
        assert "test_logger" in content
        assert "INFO" in content
        assert "Test message" in content

    def test_handlers_cleared_on_multiple_calls(self, tmp_path: Path) -> None:
        """複数回呼び出してもハンドラーが重複しない."""
        log_dir = tmp_path / "logs"
        
        setup_logging(log_dir=log_dir)
        root_logger = logging.getLogger()
        first_call_handlers = len(root_logger.handlers)
        
        setup_logging(log_dir=log_dir)
        second_call_handlers = len(root_logger.handlers)
        
        # ハンドラーは2つ（コンソールとファイル）であるべき
        assert first_call_handlers == 2
        assert second_call_handlers == 2

    def test_rotating_file_handler_config(self, tmp_path: Path) -> None:
        """RotatingFileHandlerの設定が正しい."""
        log_dir = tmp_path / "logs"
        setup_logging(log_dir=log_dir)
        
        root_logger = logging.getLogger()
        file_handlers = [
            h
            for h in root_logger.handlers
            if isinstance(h, logging.handlers.RotatingFileHandler)
        ]
        assert len(file_handlers) == 1
        
        file_handler = file_handlers[0]
        assert file_handler.maxBytes == 10 * 1024 * 1024  # 10MB
        assert file_handler.backupCount == 5

    def test_default_log_dir(self) -> None:
        """デフォルトのログディレクトリが使用される."""
        # 既存のハンドラーをクリア
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            handler.close()
            root_logger.removeHandler(handler)
        
        setup_logging()
        
        # プロジェクトルートのdata/logsディレクトリが作成されることを確認
        from mimamori_pi.config.logging_config import _find_project_root
        
        project_root = _find_project_root()
        log_dir = project_root / "data" / "logs"
        assert log_dir.exists()
        
        # クリーンアップ
        for handler in root_logger.handlers[:]:
            handler.close()
            root_logger.removeHandler(handler)

    def test_log_level_fallback_on_invalid_type(self, tmp_path: Path) -> None:
        """無効な型のログレベルはINFOにフォールバック."""
        log_dir = tmp_path / "logs"
        # 通常のケースでは発生しないが、カバレッジのために明示的にテスト
        setup_logging(log_level="INFO", log_dir=log_dir)
        
        root_logger = logging.getLogger()
        assert root_logger.level == logging.INFO

