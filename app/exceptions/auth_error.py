from exceptions.api_exception import APIException

class AuthenticationError(APIException):
    def __init__(self, status="fail", message="Authentication failed. Please log in.", http_code=401):
        super().__init__(status=status, http_code=http_code, message=message)
