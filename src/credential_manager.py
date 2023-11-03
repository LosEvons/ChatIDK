from typing import Optional
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash

class CredentialManager:
    def __init__(self, p_db):
        self.__db = p_db
        
    def username_in_database(self, username) -> bool:
        sql = text("SELECT id FROM users WHERE username=:username")
        result = self.__db.session.execute(sql, {"username":username})
        user = result.fetchone()
        if not user:
            return False
        else:
            return True
        
    def get_entry_id(self, username) -> Optional[int]:
        sql = text("SELECT id FROM users WHERE username=:username")
        result = self.__db.session.execute(sql, {"username":username})
        user = result.fetchone()
        if not user:
            return None
        else:
            return user.id
    
    def register(self, username, password) -> str:
        if self.username_in_database(username):
            return "Username already in use!"
        else:
            hash_value = generate_password_hash(password)
            sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
            self.__db.session.execute(sql, {"username":username, "password":hash_value})
            self.__db.session.commit()
            return "Account created!"
        
    def deactivate_user(self, username) -> str:
        user_id = self.get_entry_id(username)
        if not user_id:
            return "Username not found in database!"
        else:
            sql = text("UPDATE users SET visible=FALSE WHERE id=:user_id")
            self.__db.session.execute(sql, {"user_id":user_id})
            self.__db.session.commit()
            return "Account deactivated!"
                
    def login(self, username, password) -> Optional[str]:
        sql = text("SELECT id, password, visible FROM users WHERE username=:username")
        result = self.__db.session.execute(sql, {"username":username})
        user = result.fetchone()
        if not user:
            return "Bad username!"
        else:
            hash_value = user.password
            if check_password_hash(hash_value, password):
                return
            else:
                return "Bad password"