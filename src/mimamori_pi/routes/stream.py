"""ストリーミングルート."""

import logging

from flask import Blueprint, Response, jsonify

logger = logging.getLogger(__name__)

bp = Blueprint("stream", __name__)


@bp.route("/video_feed")
def video_feed() -> Response:
    """Motion JPEGストリームを提供するルート.

    Returns:
        Response: multipart/x-mixed-replace形式のMotion JPEGストリーム
    """
    from mimamori_pi.app import camera_service

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


@bp.route("/stream/start", methods=["POST"])
def stream_start() -> tuple[Response, int]:
    """ストリーミングを開始するルート.

    Returns:
        tuple[Response, int]: JSONレスポンスとステータスコード
    """
    from mimamori_pi.app import camera_service

    try:
        camera_service.start()
        logger.info("Stream started via API")
        return jsonify({"status": "success", "message": "Stream started"}), 200
    except RuntimeError as e:
        logger.error(f"Failed to start stream: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@bp.route("/stream/stop", methods=["POST"])
def stream_stop() -> tuple[Response, int]:
    """ストリーミングを停止するルート.

    Returns:
        tuple[Response, int]: JSONレスポンスとステータスコード
    """
    from mimamori_pi.app import camera_service

    try:
        camera_service.stop()
        logger.info("Stream stopped via API")
        return jsonify({"status": "success", "message": "Stream stopped"}), 200
    except Exception as e:
        logger.error(f"Failed to stop stream: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

