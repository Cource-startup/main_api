import traceback
from models.main_model import MainModel
from exceptions.main_exception import MainException
from exceptions.system_error import ServerError
from flask import jsonify, make_response

class MainController:
    def __call__(self, func):
        """
        Automatically wrap responses returned by controller methods.
        :param func: The controller method.
        """
        def wrapped_method(*args, **kwargs):
            # Call the original method and get the result

            try:
                # Execute the target function
                raw_response = func(*args, **kwargs)
            except MainException as e: 
                # use api exception logic
                raise e
            except BaseException as e:
                # handle any other errors
                raise ServerError(
                    type=type(e).__name__,       # Type of exception (e.g., ZeroDivisionError)
                    message=str(e),              # Exception message
                    traceback=traceback.format_exc()  # Full traceback as a string
                ) 

            # Filter fields for models or lists of models
            if isinstance(raw_response, MainModel):
                raw_response = raw_response.filter_fields(user=getattr(g, 'current_user', None))
            elif isinstance(raw_response, list) and all(isinstance(item, MainModel) for item in raw_response):
                raw_response = [item.filter_fields(user=getattr(g, 'current_user', None)) for item in raw_response] 
                 
            # Format the result into a standard response
            response_body = {
                "status": "success",
                "data": raw_response
            }

            # Return the Flask response object
            response = make_response(jsonify(response_body), 200)
            response.headers["Content-Type"] = "application/json"
            response.headers["Custom-Header"] = "MyCustomHeaderValue"
            return response

        return wrapped_method
