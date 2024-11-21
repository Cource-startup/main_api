from exceptions.api_exception import APIException

class FatalError(APIException):
    def __init__(self, message="An unexpected error occurred. Please try again later.", http_code=500, details=None):
        super().__init__(status="error", message=message, http_code=http_code, details=details)
