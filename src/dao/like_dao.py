from src.config import supabase

class LikeDAO:
    def add_like(self, like_data):
        return supabase.table("likes").insert(like_data).execute()

    def count_likes(self, blog_id):
        res = supabase.table("likes").select("id").eq("blog_id", blog_id).execute()
        return len(res.data) if res.data else 0
