from sqlalchemy.sql import text

class Message:
    def __init__(self, id: int, uid: int, cid: int, text: str, ts: str) -> None:
        self.id = id
        self.uid = uid
        self.cid = cid
        self.text = text
        self.ts = ts

class MessageManager:
    def get_messages(cls, chat, db) -> list[Message]:
        sql = text("SELECT id, user_id, chat_id, content, created_at FROM messages WHERE chat_id=:chat_id")
        result = db.session.execute(sql, {"chat_id":chat.id})
        raw_messages = result.fetchall()
        if not raw_messages:
            raise Exception("No messages found in database!")
        messages = []
        for message in raw_messages:
            messages.append(
                Message(
                    message.id, message.user_id, message.chat_id,
                    message.content, message.created_at
                    )
                )
        return messages
    
    def add_message(cls, uid, cid, text, db) -> None:
        sql = text("INSERT INTO messages (user_id, chat_id, content) VALUES (:uid, :cid, :text)")
        db.session.execute(sql, {"cid":uid, "cid":cid, "text":text})
        db.session.commit()