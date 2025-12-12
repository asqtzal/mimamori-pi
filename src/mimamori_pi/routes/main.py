"""メインルート."""

from flask import render_template

from mimamori_pi.app import app


@app.route("/")
def index() -> str:
    """メインページをレンダリングするルート.

    Returns:
        str: レンダリングされたHTML
    """
    return render_template("index.html")

