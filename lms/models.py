from tinydb import TinyDB, Query

db = TinyDB('db.json')
user = db.table('user')

class User:
    def __init__(self, username, password, email, id):
        self.username = username
        self.password = password
        self.email = email
        self.id = id

    def save(self):
        user.insert({'username': self.username, 'password': self.password, 'email': self.email, 'id': self.id})

    @staticmethod
    def get(username):
        User = Query()
        return user.search(User.username == username)

    @staticmethod
    def get_by_id(id):
        User = Query()
        return user.search(User.id == id)

    @staticmethod
    def get_all():
        return user.all()

    @staticmethod
    def delete(username):
        User = Query()
        user.remove(User.username == username)

    @staticmethod
    def update(username, password, email):
        User = Query()
        user.update({'username': username, 'password': password, 'email': email}, User.username == username)
