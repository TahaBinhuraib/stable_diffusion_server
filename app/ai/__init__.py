# import and register blueprints
from flask import Blueprint

ai = Blueprint("ai", __name__)

# import any flask extension specific to this module

# import views
from app.ai import views
