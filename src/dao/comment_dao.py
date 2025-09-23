from src.config import supabase

class CommentDAO:
    def add_comment(self, comment_data):
        return supabase.table("comments").insert(comment_data).execute()

    def get_comments(self, blog_id):
        return supabase.table("comments").select("*").eq("blog_id", blog_id).execute().data
