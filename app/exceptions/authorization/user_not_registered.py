from exceptions.authorization_error import AuthorizationError

class UserNotRegistered(AuthorizationError):
    def __init__(self, user_notification = "User not registered yet!"):
        super().__init__(user_notification)
