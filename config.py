import logging
import os

# set the base directory
basedir = os.path.abspath(os.path.dirname(__name__))


# Create the development config
class DevelopmentConfig:
    DEBUG = True
    LOGGING = logging.DEBUG


ENV_CONFIG = {
    "development": DevelopmentConfig,
}
