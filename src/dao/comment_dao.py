from src.config import supabase

class CommentDAO:
    def add_comment(self, data):
        return supabase.table("comments").insert(data).execute()

    def get_comments(self, blog_id):
        comments_res = supabase.table("comments").select("*").eq("blog_id", blog_id).execute()
        comments = comments_res.data if comments_res.data else []
        
        for c in comments:
            user_res = supabase.table("user_profile").select("name").eq("id", c["user_id"]).execute()
            c["username"] = user_res.data[0]["name"] if user_res.data else "Unknown"
        return comments
