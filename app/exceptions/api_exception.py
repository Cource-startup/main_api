from core.api_log import APILog

class APIException(Exception):
    def __init__(self, status="error", message="An error occurred", http_code=400, details=None):
        self.status = status
        self.message = message
        self.http_code = http_code
        self.details = details

    def to_dict(self):
        response = {
            "status": self.status,
            "message": self.message,
        }
        if self.details:
            response["details"] = self.details
            
        return response

    def log(self):
        logger = APILog()
        logger.log_error(f"{self.status.upper()} ({self.http_code}): {self.message} | Details: {self.details}")
