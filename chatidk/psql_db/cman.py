from typing import Optional
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash

from .user import User

class CredentialManager:
    def __init__(self, p_db):
        self.__db = p_db
    
    def __get_user(self, username) -> Optional[User]:
        sql = text("SELECT id, username, password FROM users WHERE username=:username AND visible=TRUE")
        result = self.__db.session.execute(sql, {"username":username})
        user = result.fetchone()
        if not user:
            return None
        else:
            return User(user.id, user.username, user.password)
    
    def register(self, username, password) -> Optional[str]:
        if self.__get_user(username):
            return "Username already in use!"
        else:
            hash_value = generate_password_hash(password)
            sql = text("INSERT INTO users (username, password, visible) VALUES (:username, :password, :visible)")
            self.__db.session.execute(sql, {"username":username, "password":hash_value, "visible":True})
            self.__db.session.commit()
            return
        
    def deactivate_user(self, username) -> Optional[str]:
        user = self.__get_user(username)
        if not user:
            return "Username not found in database!"
        else:
            sql = text("UPDATE users SET visible=FALSE WHERE id=:user_id")
            self.__db.session.execute(sql, {"user_id":user.id})
            self.__db.session.commit()
            return
                
    def login(self, username, password) -> Optional[str]:
        user = self.__get_user(username)
        if not user:
            return "Bad username!"
        else:
            hash_value = user.password
            if check_password_hash(hash_value, password):
                return
            else:
                return "Bad password"