from src.config import supabase

class BlogDAO:
    def create_blog(self, blog_data):
        res = supabase.table("blogs").insert(blog_data).execute()
        return res.data

    def list_blogs(self):
        res = supabase.table("blogs").select("*").execute()
        return res.data if res.data else []

    def search_blogs(self, keyword):
        res = supabase.table("blogs").select("*").ilike("title", f"%{keyword}%").execute()
        return res.data if res.data else []

    def get_blog_by_id(self, blog_id):
        res = supabase.table("blogs").select("*").eq("id", blog_id).execute()
        if res.data and len(res.data) > 0:
            return res.data[0]
        return None

    def delete_blog(self, blog_id):
        res = supabase.table("blogs").delete().eq("id", blog_id).execute()
        return res.data is not None
