"""ロギング設定モジュール."""

import logging
import logging.handlers
import os
from pathlib import Path


def setup_logging(log_level: str | None = None, log_dir: Path | None = None) -> None:
    """ロギング設定を初期化.

    コンソールとファイルの両方にログを出力します。
    ログレベルは環境変数 MIMAMORI_PI_LOG_LEVEL から読み込みます。

    Args:
        log_level: ログレベル（DEBUG, INFO, WARNING, ERROR, CRITICAL）。
                   Noneの場合は環境変数から読み込む。
        log_dir: ログファイルを保存するディレクトリ。
                 Noneの場合はプロジェクトルートの data/logs を使用。
    """
    # ログレベルの設定
    if log_level is None:
        log_level = os.getenv("MIMAMORI_PI_LOG_LEVEL", "INFO")
    
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    if not isinstance(numeric_level, int):
        numeric_level = logging.INFO

    # ログディレクトリの設定
    if log_dir is None:
        project_root = _find_project_root()
        log_dir = project_root / "data" / "logs"
    
    # ログディレクトリの作成
    log_dir.mkdir(parents=True, exist_ok=True)

    # ログフォーマットの設定
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # ルートロガーの設定
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)

    # 既存のハンドラーをクリア（重複を防ぐ）
    # ハンドラーをクローズしてから削除
    for handler in root_logger.handlers[:]:
        handler.close()
        root_logger.removeHandler(handler)

    # コンソールハンドラーの設定
    console_handler = logging.StreamHandler()
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # ファイルハンドラーの設定（ログローテーション対応）
    log_file = log_dir / "mimamori-pi.log"
    file_handler = logging.handlers.RotatingFileHandler(
        filename=str(log_file),
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(numeric_level)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)


def _find_project_root() -> Path:
    """プロジェクトルートディレクトリを検出.

    Returns:
        プロジェクトルートのPathオブジェクト。
    """
    current = Path(__file__).resolve()
    # src/mimamori_pi/config/logging_config.py から プロジェクトルートへ
    # 4階層上に移動
    for _ in range(4):
        current = current.parent
    return current

