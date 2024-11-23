from exceptions.main_exception import MainException

class AuthorizationError(MainException):
    def __init__(
            self,
            message="User Unauthorized!",
            user_notification=None,
        ):

        super().__init__(
            user_notification=user_notification, 
            message=message, 
            http_code=401,
        )
