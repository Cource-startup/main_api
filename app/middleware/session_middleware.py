from exceptions.authorization_error import AuthorizationError
from flask import session
from exceptions.authorization_error import AuthorizationError


class SessionMiddleware:
    def __init__(self, router_rules):
        """
        Initialize the middleware with router rules.
        """
        self.router_rules = {rule["rule"]: rule for rule in router_rules}

    def process_request(self, rule, request):
        """
        Validate the session for protected routes.
        """
        # Get route configuration
        route_config = self.router_rules.get(rule, {})

        # Skip validation if the route is marked as authorization_not_required
        if route_config.get("authorization_not_required", False):
            return None

        # Check if the session is valid
        user_id = session.get("user_id")
        if not user_id:
            raise AuthorizationError(message="Unauthorized: Session is missing or expired.")

        # If needed, add extra validation here (e.g., token match, expiry checks)
        return None  # Proceed with the request if the session is valid
