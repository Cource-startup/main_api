from exceptions.conflict_error import ConflictError


class UserAlreadyRegistered(ConflictError):
    def __init__(self, user_notification="User already registered", message=None,):
        super().__init__(user_notification=user_notification, message=message)
