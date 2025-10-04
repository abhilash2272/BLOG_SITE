from src.config import supabase

class LikeDAO:
    def like_blog(self, blog_id, user_id):
        return supabase.table("likes").insert({"blog_id": blog_id, "user_id": user_id}).execute()

    def count_likes(self, blog_id):
        res = supabase.table("likes").select("*").eq("blog_id", blog_id).execute()
        return len(res.data) if res.data else 0
