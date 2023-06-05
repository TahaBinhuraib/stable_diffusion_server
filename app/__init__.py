from config import ENV_CONFIG
from flask import Flask


def create_app(name="production"):
    app = Flask(__name__)
    app.config.from_object(ENV_CONFIG[name])
    print(f"initializing env: {name}")

    # register main
    from app.main import main as main_bp

    app.register_blueprint(main_bp)

    # register blueprints of applications
    # register error blueprint
    from app.ai import ai as ai_bp

    app.register_blueprint(ai_bp)

    # register error blueprint
    from app.errors.handlers import errors as errors_bp

    app.register_blueprint(errors_bp)

    return app