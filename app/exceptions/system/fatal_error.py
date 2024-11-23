from exceptions.main_exception import MainException

class FatalError(SystemError):
    def __init__(self):
        super().__init__(
            message="An unexpected error occurred. Please try again later.", 
            http_code=500, 
        )
