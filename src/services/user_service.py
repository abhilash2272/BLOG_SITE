from passlib.hash import bcrypt as passlib_bcrypt
from src.dao.user_dao import UserDAO

class UserService:
    def __init__(self):
        self.dao = UserDAO()

    def signup(self, name, email, password):
        """Create a new user with hashed password"""
        hashed = passlib_bcrypt.hash(password)
        return self.dao.create_user({
            "name": name,
            "email": email,
            "password": hashed
        })

    def login(self, email, password):
        """Verify user login"""
        user = self.dao.get_user_by_email(email)
        if user and passlib_bcrypt.verify(password, user["password"]):
            return user
        return None

    def update_profile(self, user_id, name=None, password=None):
        """Update user profile"""
        data = {}
        if name:
            data["name"] = name
        if password:
            data["password"] = passlib_bcrypt.hash(password)
        return self.dao.update_user(user_id, data)
