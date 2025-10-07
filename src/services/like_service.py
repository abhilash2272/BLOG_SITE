from src.dao.like_dao import LikeDAO
from src.dao.blog_dao import BlogDAO

class LikeService:
    def __init__(self):
        self.dao = LikeDAO()
        self.blog_dao = BlogDAO()

    def like_blog(self, blog_id, user_id):
        blog = self.blog_dao.get_blog_by_id(blog_id)
        if not blog:
            return {"message": f"No blog found with ID {blog_id}"}
        return self.dao.like_blog(blog_id, user_id)

    def count_likes(self, blog_id):
        blog = self.blog_dao.get_blog_by_id(blog_id)
        if not blog:
            return 0
        return self.dao.count_likes(blog_id)
