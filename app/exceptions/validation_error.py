from exceptions.main_exception import MainException

class ValidationError(MainException):
    def __init__(
            self,
            user_notification=None,
            message="Unprocessable Data.", 
            details=None,
        ):
        super().__init__(
            user_notification=user_notification,
            message=message,
            http_code=422, 
            details=details,
        )
