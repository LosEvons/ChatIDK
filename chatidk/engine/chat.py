from .user import User
from .message import MessageManager
from sqlalchemy.sql import text

class Chat:
    def __init__(self, id: int, u1: User, u2: User) -> None:
        self.id = id
        self.u1 = u1
        self.u2 = u2

class ChatManager:
    def __init__(self, db):
        self.__db = db
        
    def get_chat(self, u1: User, u2: User) -> Chat:
        sql = text("SELECT id, user1_id, user2_id FROM chats WHERE (user1_id=:u1id OR user1_id=:u2id) AND (user2_id=:u1id OR user2_id=:u2id)")
        result = self.__db.session.execute(sql, {"u1id":u1.id, "u2id":u2.id})
        chat = result.fetchone()
        if not chat:
            raise Exception("No chat found in database!")
        else:
            return Chat(chat.id, chat.user1_id, chat.user2_id)
    
    def create_chat(self, u1: User, u2: User) -> Chat:
        sql = text("INSERT INTO chats (user1_id, user2_id) VALUES (:u1id, :u2id)")
        self.__db.session.execute(sql, {"u1id":u1.id, "u2id":u2.id})
        self.__db.session.commit()
        return self.get_chat(u1, u2, self.__db)