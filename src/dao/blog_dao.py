from src.config import supabase

class BlogDAO:
    def create_blog(self, data):
        return supabase.table("blogs").insert(data).execute()

    def list_blogs(self):
        res = supabase.table("blogs").select("*").execute()
        return res.data if res.data else []

    def search_blogs(self, keyword):
        res = supabase.table("blogs").select("*").ilike("title", f"%{keyword}%").execute()
        return res.data if res.data else []

    def get_blog_by_id(self, blog_id):
        res = supabase.table("blogs").select("*").eq("id", blog_id).execute()
        return res.data[0] if res.data else None

    def delete_blog(self, blog_id):
        return supabase.table("blogs").delete().eq("id", blog_id).execute()
