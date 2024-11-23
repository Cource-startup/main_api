from flask import jsonify
from core.api_log import APILog
import traceback

class ExceptionHandler:
    log = APILog()

    @staticmethod
    def handle_exception(e):
        """Main exception handling logic."""
        from exceptions.main_exception import MainException
        if isinstance(e, MainException):
            e.log()
            return jsonify(e.to_dict()), e.http_code
        return ExceptionHandler._handle_generic_exception(e)

    @staticmethod
    def _handle_generic_exception(e):
        """Handle non-API exceptions."""
        ExceptionHandler.log.log_exception(e)
        traceback.print_exc()
        return jsonify({
            "status": "error",
            "message": "An unexpected server error."
        }), 500
