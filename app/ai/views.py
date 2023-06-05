from app.ai import ai, generator
from flask import request


@ai.route("/ai/stablediff", methods=["GET", "POST"])
def stable_diff():
    """Get stable diffusion outputs and send as a file"""
    return generator.painter.text2img(request.json)
