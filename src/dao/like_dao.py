from src.config import supabase

class LikeDAO:
    def like_blog(self, blog_id, user_id):
        # Prevent duplicate likes
        existing = supabase.table("likes").select("*").eq("blog_id", blog_id).eq("user_id", user_id).execute()
        if existing.data:
            return {"error": {"message": "You have already liked this blog!"}}
        return supabase.table("likes").insert({"blog_id": blog_id, "user_id": user_id}).execute()

    def count_likes(self, blog_id):
        res = supabase.table("likes").select("*", count="exact").eq("blog_id", blog_id).execute()
        return res.count if res.count else 0
