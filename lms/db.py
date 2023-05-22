from tinydb import TinyDB
from tinydb.table import Document

class Database:
    def __init__(self) -> None:
        self.db = TinyDB('db.json', indent=4)
        self.users = self.db.table('users')
        self.temp_user_data = self.db.table('user_data')
        self.status = "other"
        self.status_send_url = "other"
    
    def check_user(self, chat_id: int):
        if self.users.get(doc_id=chat_id):
            return True
        else:
            return False
        
    def add_user(self, data:dict, chat_id: int):
        if not self.check_user(chat_id):
            self.users.insert(Document(data, doc_id=chat_id))
        else:
            return False
    
    def get_user(self, chat_id: int):
        return self.users.get(doc_id=chat_id)
    
    # get all users
    def get_users(self):
        return self.users.all()
    
    def add_temp_user_data(self, data: dict, chat_id: int):
        if not self.temp_user_data.get(doc_id=chat_id):
            self.temp_user_data.insert(Document(data, doc_id=chat_id))
        else:
            return False
        
    def temp_user_data_get(self, chat_id: int):
        return self.temp_user_data.get(doc_id=chat_id)
    
    def temp_user_data_update(self, data: dict, chat_id: int):
        self.temp_user_data.update(data, doc_ids=[chat_id])
    
    def temp_user_data_remove(self, chat_id: int):
        self.temp_user_data.remove(doc_ids=[chat_id])