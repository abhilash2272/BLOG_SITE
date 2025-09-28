from passlib.hash import bcrypt
from src.dao.user_dao import UserDAO

class UserService:
    def __init__(self):
        self.dao = UserDAO()

    def signup(self, name, email, password):
        hashed = bcrypt.hash(password)
        return self.dao.create_user({"name": name, "email": email, "password": hashed})

    def login(self, email, password):
        user = self.dao.get_user_by_email(email)
        if user and bcrypt.verify(password, user["password"]):
            return user
        return None

    def update_profile(self, user_id, name=None, password=None):
        data = {}
        if name:
            data["name"] = name
        if password:
            data["password"] = bcrypt.hash(password)
        return self.dao.update_user(user_id, data)
