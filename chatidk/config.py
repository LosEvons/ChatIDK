class Config:
    SECRET_KEY = <your secret key>
    SQLALCHEMY_DATABASE_URI = <your database uri>
    Debug = False
    UPLOAD_FOLDER = "uploads"
    MAX_CONTENT_PATH = 10000000
    
class TestConfig:
    SECRET_KEY = <your secret key>
    SQLALCHEMY_DATABASE_URI = <your database uri>
    TESTING = True
    UPLOAD_FOLDER = "uploads"
    MAX_CONTENT_PATH = 10000000