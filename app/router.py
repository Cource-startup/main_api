from middleware import ValidationMiddleware
from controllers import UserController
from controllers import AuthController

# Router rules with validation
router_rules = [
    {
        "rule": "/", 
        "methods": ["GET"], 
        "view_func": lambda: "Hello worldddddd!",
        "authorization_not_required": True,
    },
    # Google Auth
    {
        "rule": "/user_auth", 
        "methods": ["POST"], 
        "view_func": AuthController.auth_controller,
        "authorization_not_required": True,
        "validation": {
            "fields": {
                "service_auth_id_field_name": {
                    ValidationMiddleware.IS_REQUIRED: True,
                    ValidationMiddleware.IS_NULLABLE: False,
                },
                "service_auth_code": {
                    ValidationMiddleware.IS_REQUIRED: True,
                    ValidationMiddleware.IS_NULLABLE: False,
                    ValidationMiddleware.REGEXP_PATTERN: r"^\S{30,100}$",
                }
            }
        }
    },
    {
        "rule": "/register_user", 
        "methods": ["POST"], 
        "view_func": UserController.register_user,
        "authorization_not_required": True,
        "validation": {
            "fields": {
                "service_auth_id_field_name": {
                    ValidationMiddleware.IS_REQUIRED: True,
                    ValidationMiddleware.IS_NULLABLE: False,
                },
                "service_auth_code": {
                    ValidationMiddleware.IS_REQUIRED: True,
                    ValidationMiddleware.IS_NULLABLE: False,
                    ValidationMiddleware.REGEXP_PATTERN: r"^\S{30,100}$",
                },
                "login": {
                    ValidationMiddleware.IS_REQUIRED: True,
                    ValidationMiddleware.IS_NULLABLE: False,
                    ValidationMiddleware.REGEXP_PATTERN: r"^[a-z_]{5,15}$",
                },
            },
        },
    },

    # User API
    {
        "rule": "/update_user/<int:id>", 
        "methods": ["POST"], 
        "view_func": UserController.update_user,
        "authorization_not_required": False,
        "validation": {
            "fields": {
                "login": {
                    ValidationMiddleware.IS_REQUIRED: True,
                    ValidationMiddleware.IS_NULLABLE: True,
                },
                "user_name": {
                    ValidationMiddleware.IS_REQUIRED: True,
                    ValidationMiddleware.IS_NULLABLE: True,
                },
                "avatar": {
                    ValidationMiddleware.IS_REQUIRED: False,
                    ValidationMiddleware.IS_NULLABLE: True,
                    ValidationMiddleware.REGEXP_PATTERN: r"^.*\.(jpg|jpeg|png|gif)$"  # Must be an image file
                },
            }
        },
    },

    {
        "rule": "/user/<int:user_id>/avatar", 
        "methods": ["GET"], 
        "view_func": UserController.get_user_avatar,
    },

    {
        "rule": "/get_users", 
        "methods": ["GET"], 
        "view_func": UserController.get_users,
    },
]
