from exceptions.system.file_error import FileError
from services.file_service import FileService
from exceptions.conflict.user_not_found import UserNotFound
from exceptions.system.fatal_error import FatalError
from models import User
from config import current_config
from sqlalchemy import select
from db import db
from flask import send_file


class UserService:
    # Define file_service as a class-level attribute
    file_service = FileService(
        upload_folder=current_config.UPLOAD_FOLDER,
        allowed_extensions=current_config.ALLOWED_EXTENSIONS,
        max_file_size=current_config.MAX_CONTENT_LENGTH,
    )

    def get_users_by(field = None, field_value = None, from_number = None, count = None):

        statement  = select(User).where(getattr(User, field) == field_value)

        users = []
        for row in db.session.execute(statement):
            users.append(row.User.toDict())    

        return users
    
    def get_user_by_id(user_id):
        return __class__.get_users_by("id", user_id)[0]
    
    def create_update_user_by(unique_user_field_name, user_data):
        users = __class__.get_users_by(unique_user_field_name, user_data[unique_user_field_name])
        amount_of_users = len(users)

        if amount_of_users == 0:
            user = User()
        elif amount_of_users == 1:
            user = users[0]
        else:
            raise FatalError(f'Error! {amount_of_users} users have been found by the unique field "{unique_user_field_name}"')


        for field_name in user.mutable_fields:
            setattr(user, field_name, user_data.get(field_name, None))
        
        db.session.add(user)
        db.session.commit()

        return __class__.get_user_by_id(user.id)

    def update_user_by_id(user_id, request_body):
        user = User.query.get(user_id)

        for field_key, field_value in request_body.items():
            setattr(user, field_key, field_value)
        db.session.commit()

        return __class__.get_user_by_id(user_id)
    
    @staticmethod
    def update_user_by_id(user_id, request_body, avatar=None):
        """
        Update user by ID, including handling avatar upload.

        :param user_id: ID of the user to update.
        :param request_body: Dictionary of fields to update.
        :param avatar: File object for the avatar, if provided.
        :return: Updated user data.
        """
        user = User.query.get(user_id)
        if not user:
            raise UserNotFound()

        # Update fields from the request body
        for field_key, field_value in request_body.items():
            setattr(user, field_key, field_value)

        # Handle avatar upload if provided
        if avatar:
            try:
                file_path = UserService.file_service.save_file(avatar)  # Save file
                UserService.file_service.validate_and_resize_image(file_path)  # Validate and resize
                user.avatar_path = file_path
            except FileError as e:
                raise e

        # Commit changes to the database
        db.session.commit()

        # Return the updated user data
        return __class__.get_user_by_id(user_id)


    def delete_user_by_id(user_id):
        user = User.query.get(user_id)
        if user == None:
            return ('User with Id "{}" is not found!').format(user_id)

        db.session.delete(user)
        db.session.commit()
        return ('User with Id "{}" deleted successfully!').format(user_id)
    
    @staticmethod
    def get_user_avatar(user_id):
        user = User.query.get(user_id)
        if not user:
            raise UserNotFound()
        return send_file(user.avatar_path, mimetype="image/jpeg")

    @staticmethod
    def upload_user_avatar(user_id, avatar):
        """
        Upload a user's avatar.
        """
        user = User.query.get(user_id)
        if not user:
            raise UserNotFound()

        if avatar:
            try:
                file_path = UserService.file_service.save_file(avatar)  # Use instance attribute
                UserService.file_service.validate_and_resize_image(file_path)  # Validate and resize
                user.avatar = file_path  # Update the avatar path for the user
            except FileError as e:
                raise e

        db.session.commit()
        return UserService.get_user_by_id(user_id)