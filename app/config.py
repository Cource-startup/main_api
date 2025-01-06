import os

class Config:
    FLASK_RUN_RELOAD=0
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    TRACK_STORAGE_FOLDER = "track_storage"
    MAX_CONTENT_LENGTH = 1024 * 1024 * 25 # 25 mb
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    CLIENT_SECRET_FILE = "../client_secret.json"
    CSRF_BACKEND_TOKEN = os.getenv('CSRF_BACKEND_TOKEN')
    SESSION_LIFE_TIME = 10 # in minutes
    SECRET_KEY = os.getenv('SESSION_SECRET_KEY')
    SESSION_TYPE = "filesystem"
    GOOGLE_SIGN_IN_ACCOUNT = 'google_sign_in_account'
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DEVELOPMENT_DATABASE_URL")
    UPLOAD_FOLDER = "dev_file_storage"
    OAUTHLIB_INSECURE_TRANSPORT = "1"

class TestingConfig(Config):
    DEBUG=False
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL")
    OAUTHLIB_INSECURE_TRANSPORT = "1"

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("PRODUCTION_DATABASE_URL")

config_dict = {
    "dev": DevelopmentConfig,
    "test": TestingConfig,
    "prod": ProductionConfig
}

current_config = config_dict[os.getenv("CONFIG_MODE")]