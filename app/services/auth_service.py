from exceptions.authorization.user_not_registered import UserNotRegistered
from exceptions.conflict_error import ConflictError
from exceptions.not_found_error import NotFoundError
from services.session_service import SessionService
from exceptions import AuthorizationError, FatalError
from services.google_auth_service import GoogleAuthService
from services import UserService

class AuthService:
        
    def get_authentication_and_user_by_service(service_auth_id_field_name, service_auth_code):

        match service_auth_id_field_name:
            case GoogleAuthService.ID_FIELD_KEY:
                auth_data = GoogleAuthService.get_google_data(auth_code=service_auth_code)
            case False: # for other auth services 
                pass 
            case _:
                raise NotFoundError(message="Unexpected type of authentication.")
        
        users = UserService.get_users_by(service_auth_id_field_name, auth_data[service_auth_id_field_name])

        if len(users) > 1:
            raise ConflictError(message="More than one user found by authentication_service id!")
        
        return auth_data, users[0] if users else None
    
    def auth_user(service_auth_id_field_name, service_auth_code):
        _, user = __class__.get_authentication_and_user_by_service(service_auth_id_field_name, service_auth_code)
        if user:
            return {
                "user": user,
                "session_token": SessionService.set_session(user["id"])
            }
        else:
            raise UserNotRegistered()
    
    def register_user(service_auth_id_field_name, service_auth_code, login):
        if UserService.get_users_by("login", login):
            raise ConflictError(user_notification=f"User under login: {login} already exists.")

        auth_data, user = __class__.get_authentication_and_user_by_service(service_auth_id_field_name, service_auth_code)
        
        if user:
            raise ConflictError(message=f"User under {service_auth_id_field_name}: {auth_data[service_auth_id_field_name]} already exists.")

        user = UserService.create_update_user_by(
            service_auth_id_field_name, 
            {service_auth_id_field_name: auth_data[service_auth_id_field_name], "login": login}
        )
        
        if user:
            return {
                "user": user,
                "session_token": SessionService.set_session(user["id"])
            }
        else:
            raise UserNotRegistered()
