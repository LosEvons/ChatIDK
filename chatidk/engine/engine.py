from .user import UserManager
from .chat import ChatManager

class Engine:
    def __init__(self, db):
        self.um = UserManager(db)
        self.cm = ChatManager(db)