from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash

class User:
    def __init__(self, id: int, un: str, pw: str):
        self.id = id
        self.un = un
        self.pw = pw
        
    def __str__(self) -> str:
        return self.un
    
class UserManager:
    def __init__(self, db):
        self.__db = db
        self.au: User = None

    def get_users(self) -> list[User]:
        sql = text("SELECT id, username, password FROM users WHERE visible=TRUE")
        result = self.__db.session.execute(sql)
        raw_users = result.fetchall()
        if not raw_users:
            return None
        users = []
        for user in raw_users:
            users.append(User(user.id, user.username, user.password))
        return users
    
    def get_other_users(self) -> list[User]:
        users = self.get_users()
        if self.au and users:
            for user in users:
                if user.id == self.au.id:
                    users.remove(user)
        return users
    
    def get_user(self, username: str) -> User:
        sql = text("SELECT id, username, password FROM users WHERE username=:username AND visible=TRUE")
        result = self.__db.session.execute(sql, {"username":username})
        user = result.fetchone()
        if not user:
            return None
        else:
            return User(user.id, user.username, user.password)
        
    def register(self, username, password) -> str:
        if self.get_user(username):
            return "Username already in use!"
        else:
            hash_value = generate_password_hash(password)
            sql = text("INSERT INTO users (username, password, visible) VALUES (:username, :password, :visible)")
            self.__db.session.execute(sql, {"username":username, "password":hash_value, "visible":True})
            self.__db.session.commit()
            return
        
    def deactivate_user(self, user) -> str:
        if not user:
            return "Username not found in database!"
        else:
            sql = text("UPDATE users SET visible=FALSE WHERE id=:uid")
            self.__db.session.execute(sql, {"uid":user.id})
            self.__db.session.commit()
            return
                
    def login(self, username, password) -> str:
        user = self.get_user(username)
        if not user:
            return "Bad username!"
        else:
            hash_value = user.pw
            if check_password_hash(hash_value, password):
                self.au = user
                return
            else:
                return "Bad password"
    
    def logout(self) -> None:
        self.au = None