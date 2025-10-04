from src.config import supabase

class UserDAO:
    def create_user(self, data):
        return supabase.table("user_profile").insert(data).execute()

    def get_user_by_email(self, email):
        res = supabase.table("user_profile").select("*").eq("email", email).execute()
        if res.data:
            return res.data[0]
        return None

    def update_user(self, user_id, data):
        return supabase.table("user_profile").update(data).eq("id", user_id).execute()
