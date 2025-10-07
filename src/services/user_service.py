from src.dao.user_dao import UserDAO

class UserService:
    def __init__(self):
        self.dao = UserDAO()

    def signup(self, name, email, password):
        try:
            return self.dao.create_user({"name": name, "email": email, "password": password})
        except Exception as e:
            err = str(e)
            if "duplicate key value" in err or "already exists" in err:
                return {"error": "Email already exists. Please login instead."}
            return {"error": "Something went wrong during signup."}

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
