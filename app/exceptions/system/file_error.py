from exceptions.system_error import ServerError

class FileError(SystemError):
    def __init__(self, message="File error occurred"):
        super().__init__(
            message=message,  # Use the provided message
            http_code=500, 
        )
