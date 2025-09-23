from src.config import supabase

class LikeDAO:
    def add_like(self, like_data):
        return supabase.table("likes").insert(like_data).execute()

    def count_likes(self, blog_id):
        return len(supabase.table("likes").select("*").eq("blog_id", blog_id).execute().data)
