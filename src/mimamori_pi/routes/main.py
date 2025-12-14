"""メインルート."""

from flask import Blueprint, render_template

bp = Blueprint("main", __name__)


@bp.route("/")
def index() -> str:
    """メインページをレンダリングするルート.

    Returns:
        str: レンダリングされたHTML
    """
    return render_template("index.html")

