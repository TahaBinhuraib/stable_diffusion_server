# import the create app application factory
import os

from app import create_app
from utils import datastructures

# import the application config classes

FLASK_ENV = os.environ.get("FLASK_ENV", "development")
application = create_app(FLASK_ENV)
application.json_encoder = datastructures.EnhancedJSONEncoder

import logging

logging.basicConfig(
    level=application.config["LOGGING"],
    format="%(asctime)s [%(filename)s:%(lineno)d] %(message)s",
    datefmt="%m-%d %H:%M",
)

if __name__ == "__main__":
    application.run(host="0.0.0.0")
