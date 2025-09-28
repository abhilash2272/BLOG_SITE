import hashlib, hmac, os
from src.dao.user_dao import UserDAO

class UserService:
    def __init__(self):
        self.dao = UserDAO()

    def _hash_password(self, password: str, salt: str = None):
        if not salt:
            salt = os.urandom(16).hex()
        hashed = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode(),
            salt.encode(),
            100000
        ).hex()
        return f"{salt}${hashed}"

    def _verify_password(self, password: str, stored_hash: str):
        try:
            salt, hashed = stored_hash.split("$")
            new_hash = hashlib.pbkdf2_hmac(
                "sha256",
                password.encode(),
                salt.encode(),
                100000
            ).hex()
            return hmac.compare_digest(hashed, new_hash)
        except Exception:
            return False

    def signup(self, name, email, password):
        hashed = self._hash_password(password)
        return self.dao.create_user({
            "name": name,
            "email": email,
            "password": hashed
        })

    def login(self, email, password):
        user = self.dao.get_user_by_email(email)
        if user and self._verify_password(password, user["password"]):
            return user
        return None

    def update_profile(self, user_id, name=None, password=None):
        data = {}
        if name:
            data["name"] = name
        if password:
            data["password"] = self._hash_password(password)
        return self.dao.update_user(user_id, data)
