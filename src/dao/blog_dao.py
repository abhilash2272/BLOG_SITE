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
        return self.dao.list_blogs()

    def search_blogs(self, keyword):
        return self.dao.search_blogs(keyword)

    def delete_blog(self, blog_id):
        blog = self.dao.get_blog_by_id(blog_id)
        if blog:
            return self.dao.delete_blog(blog_id)
        return False
