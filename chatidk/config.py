class Config:
    SECRET_KEY = "b6375bad9fd2678cd48273b939fbdbb6"
    SQLALCHEMY_DATABASE_URI = "postgresql:///emilmalk"
    Debug = False
    
class TestConfig:
    SECRET_KEY = "b6375bad9fd2678cd48273b939fbdbb6"
    SQLALCHEMY_DATABASE_URI = "postgresql:///emilmalk"
    TESTING = True