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
    
    def get_message_attachment(self, msg: Message) -> str:
        sql = text("SELECT file_id FROM attachments WHERE message_id=:msg_id")
        result = self.__db.session.execute(sql, {"msg_id":msg.id})
        fid: int = result.fetchone()[0]
        if not fid:
            return None
        sql = text("SELECT filepath FROM files WHERE id=:fid")
        result = self.__db.session.execute(sql, {"fid":fid})
        attachment: str = result.fetchone()[0]
        return attachment
        
    def add_message_attachment(self, uid, cid, filepath: str) -> None:
        sql = text("SELECT filepath FROM files WHERE filepath=:filepath")
        result = self.__db.session.execute(sql, {"filepath":filepath})
        
        if not result.fetchone():
            sql = text("INSERT INTO files (filepath) VALUES (:filepath)")
            self.__db.session.execute(sql, {"filepath":filepath})
            self.__db.session.commit()
            
        sql = text("SELECT id FROM messages WHERE user_id=:uid AND chat_id=:cid ORDER BY created_at DESC LIMIT 1")
        result = self.__db.session.execute(sql, {"uid":uid, "cid":cid})
        msg_id = result.fetchone()[0]
        
        sql = text("INSERT INTO attachments (file_id, message_id) VALUES((SELECT id FROM files WHERE filepath=:filepath), :msg_id)")
        self.__db.session.execute(sql, {"filepath":filepath, "msg_id":msg_id})
        self.__db.session.commit()
        
    def has_attachment(self, msg: Message) -> bool:
        sql = text("SELECT file_id FROM attachments WHERE message_id=:msg_id")
        result = self.__db.session.execute(sql, {"msg_id":msg.id})
        fid: int = result.fetchone()
        if not fid:
            return False
        else:
            return True