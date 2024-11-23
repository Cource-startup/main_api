from exceptions.main_exception import MainException

class ConflictError(MainException):
    def __init__(
            self,
            message="The request cannot be completed because it conflicts!",
            user_notification=None,
        ):

        super().__init__(
            user_notification=user_notification, 
            message=message, 
            http_code=409,
        )
