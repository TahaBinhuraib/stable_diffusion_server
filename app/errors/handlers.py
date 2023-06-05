from flask import Blueprint

errors = Blueprint("errors", __name__)


@errors.app_errorhandler(404)
def error_404(error):
    return (
        {
            "code": 404,
            "error_type": "Page not found",
            "error_message": str(error),
        }
    ), 404


@errors.app_errorhandler(RuntimeError)
def run_time(error):
    return (
        {"code": 506, "error_type": "Runtime Error", "error_message": str(error)}
    ), 506


@errors.app_errorhandler(ValueError)
def value_error(error):
    return (
        {"code": 507, "error_type": "Value Error", "error_message": str(error)}
    ), 507


@errors.app_errorhandler(NameError)
def name_error(error):
    return ({"code": 508, "error_type": "Name Error", "error_message": str(error)}), 508


@errors.app_errorhandler(IndexError)
def index_error(error):
    return (
        {"code": 509, "error_type": "index Error", "error_message": str(error)}
    ), 509


@errors.app_errorhandler(TypeError)
def type_error(error):
    return ({"code": 510, "error_type": "Type Error", "error_message": str(error)}), 510


@errors.app_errorhandler(MemoryError)
def memory_error(error):
    return (
        {"code": 511, "error_type": "Memory Error", "error_message": str(error)}
    ), 510


@errors.app_errorhandler(KeyError)
def key_error(error):
    return ({"code": 512, "error_type": "Key Error", "error_message": str(error)}), 511