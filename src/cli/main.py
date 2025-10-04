from src.services.user_service import UserService
from src.services.blog_service import BlogService
from src.services.comment_service import CommentService
from src.services.like_service import LikeService

def main():
    user_service = UserService()
    blog_service = BlogService()
    comment_service = CommentService()
    like_service = LikeService()

    print("Welcome to Blog Nest")
    choice = input("1.Signup 2.Login: ")

    current_user = None
    if choice == "1":
        name = input("Name: ")
        email = input("Email: ")
        password = input("Password: ")
        user_service.signup(name, email, password)
        print("✅ User created!")
        return
    elif choice == "2":
        email = input("Email: ")
        password = input("Password: ")
        user = user_service.login(email, password)
        if not user:
            print("❌ Invalid credentials")
            return
        current_user = user
        print("✅ Login successful!")

    while True:
        print("""
Menu:
1.Create Blog 2.List Blogs 3.Search Blogs 4.Delete Blog
5.Add Comment 6.View Comments 7.Like Blog 8.Count Likes 9.Update Profile 10.Exit
        """)
        option = input("Choose: ")

        if option == "1":
            title = input("Title: ")
            content = input("Content: ")
            category = input("Category: ")
            blog_service.create_blog(current_user["id"], title, content, category)
            print("✅ Blog created!")

        elif option == "2":
            blogs = blog_service.list_blogs()
            if blogs:
                for b in blogs:
                    print(f"{b['id']}. {b['title']} - {b['category']} (by {b['user_id']})")
            else:
                print("No blogs found.")

        elif option == "3":
            keyword = input("Enter keyword to search: ")
            blogs = blog_service.search_blogs(keyword)
            if blogs:
                for b in blogs:
                    print(f"{b['id']}. {b['title']} - {b['category']} (by {b['user_id']})")
            else:
                print("No blogs found.")

        elif option == "4":
            blog_id = int(input("Enter blog ID to delete: "))
            res = blog_service.delete_blog(blog_id)
            print(res.get("message"))

        elif option == "5":
            blog_id = int(input("Blog ID: "))
            comment_text = input("Comment: ")
            comment_service.add_comment(blog_id, current_user["id"], comment_text)
            print("✅ Comment added!")

        elif option == "6":
            blog_id = int(input("Blog ID: "))
            comments = comment_service.get_comments(blog_id)
            if comments:
                for c in comments:
                    print(f"{c['id']}: {c['comment']} (by {c['user_id']})")
            else:
                print("No comments yet.")

        elif option == "7":
            blog_id = int(input("Blog ID: "))
            like_service.like_blog(blog_id, current_user["id"])
            print("✅ Liked!")

        elif option == "8":
            blog_id = int(input("Blog ID: "))
            print("Total Likes:", like_service.count_likes(blog_id))

        elif option == "9":
            name = input("New Name (leave blank to skip): ")
            password = input("New Password (leave blank to skip): ")
            user_service.update_profile(current_user["id"], name, password)
            print("✅ Profile updated!")

        elif option == "10":
            break

if __name__ == "__main__":
    main()
