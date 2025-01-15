from exceptions.system_error import ServerError

class FileError(SystemError):
    def __init__(self):
        super().__init__(
            message="File error occurred", 
            http_code=500, 
        )
