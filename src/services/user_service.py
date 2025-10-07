from src.config import supabase

class UserService:
    def __init__(self):
        pass

    def signup(self, name, email, password):
        # Avoid duplicate users
        existing = supabase.table("user_profile").select("*").eq("email", email).execute()
        if existing.data:
            raise Exception(f"User with email {email} already exists")
        return supabase.table("user_profile").insert({
            "name": name,
            "email": email,
            "password": password
        }).execute()

    def login(self, email, password):
        res = supabase.table("user_profile").select("*").eq("email", email).eq("password", password).execute()
        return res.data[0] if res.data else None

    def update_profile(self, user_id, name=None, password=None):
        data = {}
        if name:
            data["name"] = name
        if password:
            data["password"] = password
        return supabase.table("user_profile").update(data).eq("id", user_id).execute()
