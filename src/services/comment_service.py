from src.dao.comment_dao import CommentDAO

class CommentService:
    def __init__(self):
        self.dao = CommentDAO()

    def add_comment(self, blog_id, user_id, comment):
        return self.dao.add_comment({"blog_id": blog_id, "user_id": user_id, "comment": comment})

    def get_comments(self, blog_id):
        return self.dao.get_comments(blog_id)
