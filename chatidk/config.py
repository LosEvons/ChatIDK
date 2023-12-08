import secrets

class Config:
    SECRET_KEY = secrets.token_hex(16)
    SQLALCHEMY_DATABASE_URI = <your database url>
    Debug = False
    UPLOAD_FOLDER = "uploads"
    MAX_CONTENT_PATH = 10000000
    
class TestConfig:
    SECRET_KEY = secrets.token_hex(16)
    SQLALCHEMY_DATABASE_URI = <your database url>
    TESTING = True
    UPLOAD_FOLDER = "uploads"
    MAX_CONTENT_PATH = 10000000