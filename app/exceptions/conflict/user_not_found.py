from exceptions.conflict_error import ConflictError


class UserNotFound(ConflictError):
    def __init__(self, user_notification="The user not found", message=None,):
        super().__init__(user_notification=user_notification, message=message)
