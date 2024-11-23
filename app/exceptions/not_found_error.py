from exceptions.main_exception import MainException

class NotFoundError(MainException):
    def __init__(
            self,
            user_notification=None,
            message="The requested resource was not found.", 
            details=None
        ):
        super().__init__(
            user_notification=user_notification,
            message=message,
            http_code=404, 
            details=details
        )
