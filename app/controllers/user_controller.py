from services.auth_service import AuthService
from services import UserService
from flask import request

class UserController:
    
    def get_users():
        from_number = request.args.get('from', default=0, type=int)
        count = request.args.get('count', default=100, type=int)
        return UserService.get_users_by(from_number=from_number, count=count)
    
    def register_user():
        data = request.get_json()
        return AuthService.register_user(**data)
    
    def update_user(id):
        data = request.get_json()
        avatar = request.files.get('avatar')  # Extract file if provided
        return UserService.update_user_by_id(id, data, avatar)
    
    def get_user_avatar(user_id):
        return UserService.get_user_avatar(user_id)
    

    def upload_avatar(user_id):
        """
        Handle the avatar upload request.

        :param user_id: ID of the user to upload an avatar for.
        :return: Updated user data with the new avatar.
        """
        avatar = request.files.get('avatar')  # Extract file from the request
        # print(avatar)
        
        return UserService.upload_user_avatar(user_id, avatar)
    