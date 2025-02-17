from config import Config
from exceptions.authorization_error import AuthorizationError
from exceptions.validation_error import ValidationError
import hashlib

class CSRFMiddleware:
    def __init__(self):
        pass

    def process_request(self, rule, request):
        """
        Validate the CSRF token for protected routes.
        """
        # Skip CSRF check for safe HTTP methods
        if request.method in ["HEAD", "OPTIONS"]:
            return None

        # Get the CSRF secret from the config
        csrf_token =  str(hashlib.sha256(Config.CSRF_BACKEND_TOKEN.encode()).hexdigest())

        if not csrf_token:
            raise SystemError(message="CSRF secret not configured in application settings.")

        # Extract the CSRF token from headers or request body
        received_csrf_token = request.headers.get("CSRF-Token") or request.json.get("csrf_token")

        if not received_csrf_token:
            raise ValidationError(
                message="Missing CSRF token. Please include the token in the header or body.",
                details={"method": request.method, "path": request.path}
            )

        if received_csrf_token != csrf_token:
            raise AuthorizationError(
                message="Invalid CSRF token.",
                details={"method": request.method, "path": request.path}
            )

        # Token is valid; continue the request
        return None
