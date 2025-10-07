from src.config import supabase

class BlogDAO:
    def create_blog(self, data):
        return supabase.table("blogs").insert(data).execute()

    def list_blogs(self):
        blogs_res = supabase.table("blogs").select("*").execute()
        blogs = blogs_res.data if blogs_res.data else []

        # Add author name for each blog
        for blog in blogs:
            user_res = supabase.table("user_profile").select("name").eq("id", blog["user_id"]).execute()
            blog["author_name"] = user_res.data[0]["name"] if user_res.data else "Unknown"

        return blogs

    def search_blogs(self, keyword):
        blogs_res = supabase.table("blogs").select("*").ilike("title", f"%{keyword}%").execute()
        blogs = blogs_res.data if blogs_res.data else []

        for blog in blogs:
            user_res = supabase.table("user_profile").select("name").eq("id", blog["user_id"]).execute()
            blog["author_name"] = user_res.data[0]["name"] if user_res.data else "Unknown"

        return blogs

    def get_blog_by_id(self, blog_id):
        res = supabase.table("blogs").select("*").eq("id", blog_id).execute()
        blog = res.data[0] if res.data else None
        if blog:
            user_res = supabase.table("user_profile").select("name").eq("id", blog["user_id"]).execute()
            blog["author_name"] = user_res.data[0]["name"] if user_res.data else "Unknown"
        return blog

    def delete_blog(self, blog_id):
        return supabase.table("blogs").delete().eq("id", blog_id).execute()
