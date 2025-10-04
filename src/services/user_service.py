from src.dao.user_dao import UserDAO

class UserService:
    def __init__(self):
        self.dao = UserDAO()

    def signup(self, name, email, password):
        return self.dao.create_user({"name": name, "email": email, "password": password})

    def login(self, email, password):
        user = self.dao.get_user_by_email(email)
        if user and user["password"] == password:
            return user
        return None

    def update_profile(self, user_id, name=None, password=None):
        data = {}
        if name:
            data["name"] = name
        if password:
            data["password"] = password
        return self.dao.update_user(user_id, data)
