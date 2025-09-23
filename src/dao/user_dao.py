from src.config import supabase

class UserDAO:
    def create_user(self, user_data):
        return supabase.table("user_profile").insert(user_data).execute()

    def get_user_by_email(self, email):
        res = supabase.table("user_profile").select("*").eq("email", email).execute()
        return res.data[0] if res.data else None

    def update_user(self, user_id, update_data):
        return supabase.table("user_profile").update(update_data).eq("id", user_id).execute()
