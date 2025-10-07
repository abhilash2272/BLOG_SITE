from src.dao.comment_dao import CommentDAO
from src.dao.blog_dao import BlogDAO

class CommentService:
    def __init__(self):
        self.dao = CommentDAO()
        self.blog_dao = BlogDAO()

    def add_comment(self, blog_id, user_id, comment):
        blog = self.blog_dao.get_blog_by_id(blog_id)
        if not blog:
            return {"message": f"No blog found with ID {blog_id}"}
        return self.dao.add_comment({
            "blog_id": blog_id,
            "user_id": user_id,
            "comment": comment
        })

    def get_comments(self, blog_id):
        return self.dao.get_comments(blog_id)
