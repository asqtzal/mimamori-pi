"""ストリーミングルート."""

import logging

from flask import Response

from mimamori_pi.app import app, camera_service

logger = logging.getLogger(__name__)


@app.route("/video_feed")
def video_feed() -> Response:
    """Motion JPEGストリームを提供するルート.

    Returns:
        Response: multipart/x-mixed-replace形式のMotion JPEGストリーム
    """
    try:
        return Response(
            camera_service.generate_stream(),
            mimetype="multipart/x-mixed-replace; boundary=frame",
        )
    except RuntimeError as e:
        logger.error(f"Failed to generate video feed: {e}")
        return Response(
            f"Camera error: {e}",
            status=500,
            mimetype="text/plain",
        )


@app.route("/stream/start", methods=["POST"])
def stream_start() -> tuple[dict[str, str], int]:
    """ストリーミングを開始するルート.

    Returns:
        tuple[dict[str, str], int]: JSONレスポンスとステータスコード
    """
    try:
        camera_service.start()
        logger.info("Stream started via API")
        return {"status": "success", "message": "Stream started"}, 200
    except RuntimeError as e:
        logger.error(f"Failed to start stream: {e}")
        return {"status": "error", "message": str(e)}, 500


@app.route("/stream/stop", methods=["POST"])
def stream_stop() -> tuple[dict[str, str], int]:
    """ストリーミングを停止するルート.

    Returns:
        tuple[dict[str, str], int]: JSONレスポンスとステータスコード
    """
    try:
        camera_service.stop()
        logger.info("Stream stopped via API")
        return {"status": "success", "message": "Stream stopped"}, 200
    except Exception as e:
        logger.error(f"Failed to stop stream: {e}")
        return {"status": "error", "message": str(e)}, 500

