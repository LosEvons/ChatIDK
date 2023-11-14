from sqlalchemy.sql import text
import datetime

class Message:
    def __init__(self, id: int, uid: int, cid: int, text: str, ts: str):
        self.id = id
        self.uid = uid
        self.cid = cid
        self.text = text
        self.ts = ts

class MessageManager:
    def __init__(self, db):
        self.__db = db
        
    def get_messages(self, chat) -> list[Message]:
        sql = text("SELECT id, user_id, chat_id, content, created_at FROM messages WHERE chat_id=:chat_id")
        result = self.__db.session.execute(sql, {"chat_id":chat.id})
        raw_messages = result.fetchall()
        if not raw_messages:
            return None
        messages = []
        for message in raw_messages:
            messages.append(
                Message(
                    message.id, message.user_id, message.chat_id,
                    message.content, message.created_at
                    )
                )
        return messages
    
    def add_message(self, uid: int, cid: int, msg: str) -> None:
        sql = text("INSERT INTO messages (user_id, chat_id, content, created_at) VALUES (:user_id, :chat_id, :content, :created_at)")
        self.__db.session.execute(sql, {"user_id":uid, "chat_id":cid, "content":msg, "created_at":datetime.datetime.now()})
        self.__db.session.commit()