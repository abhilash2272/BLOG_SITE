from src.dao.like_dao import LikeDAO

class LikeService:
    def __init__(self):
        self.dao = LikeDAO()

    def like_blog(self, blog_id, user_id):
        return self.dao.add_like({"blog_id": blog_id, "user_id": user_id})

    def count_likes(self, blog_id):
        return self.dao.count_likes(blog_id)
