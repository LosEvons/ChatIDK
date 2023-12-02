from .user import UserManager
from .chat import ChatManager

class Engine:
    def __init__(self, db, uf: str):
        self.um = UserManager(db)
        self.cm = ChatManager(db)
        self.uf = uf