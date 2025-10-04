from src.dao.blog_dao import BlogDAO

class BlogService:
    def __init__(self):
        self.dao = BlogDAO()

    def create_blog(self, user_id, title, content, category):
        return self.dao.create_blog({
            "user_id": user_id,
            "title": title,
            "content": content,
            "category": category
        })

    def list_blogs(self):
        blogs = self.dao.list_blogs()
        return blogs if blogs else []

    def search_blogs(self, keyword):
        blogs = self.dao.search_blogs(keyword)
        return blogs if blogs else []

    def delete_blog(self, blog_id):
        blog = self.dao.get_blog_by_id(blog_id)
        if not blog:
            return {"message": "No blog found with this ID"}
        self.dao.delete_blog(blog_id)
        return {"message": "✅ Blog deleted!"}
