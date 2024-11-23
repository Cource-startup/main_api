from core.helper import Helper
from core.api_log import APILog

class MainException(Exception):
    def __init__(
            self, 
            status="error",
            type="error",
            user_notification=None, 
            message="An error occurred", 
            http_code=500, 
            details=None
        ):

        self.status = status
        self.type = Helper.to_snake_case(self.__class__.__name__ or type)
        self.user_notification = user_notification
        self.message = message
        self.http_code = http_code
        self.details = details

    def to_dict(self):

        error_object = {
            "type": self.type,
            "message": self.message,
        }

        if self.details:
            error_object["details"] = self.details
        if self.user_notification:
            error_object["user_notification"] = self.user_notification

        return {
            "status": self.status,
            "error": error_object
        }

    def log(self):
        logger = APILog()
        logger.log_error(f"{self.status.upper()} ({self.http_code}): {self.message} | Details: {self.details}")
