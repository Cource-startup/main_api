from config import Config
from exceptions.main_exception import MainException

class ServerError(MainException):
    def __init__(self, message="An error occurred", http_code=500, details = None):
        if not Config.DEBUG:
            super().__init__(
                message="Internal Server Error.", 
                http_code=500, 
            )
            return
        
        super().__init__(
            self, 
            message=message, 
            http_code=http_code,
            details=details
        )
