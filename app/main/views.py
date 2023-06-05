# import the main blue print instance
from app.main import main
from flask import request


@main.before_request
def limit_remote_addr():
    print(request.remote_addr)
    if request.remote_addr != "10.1.16.164":
        pass
        # abort(403)  # Forbidden


@main.route("/")
@main.route("/index")
def index():
    return "Hello from the ubuntu machine"


@main.route("/ai/gpt")
def index1():
    return "Hello from the ubuntu machine with stable diff"
