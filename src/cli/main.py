from src.services.user_service import UserService
from src.services.blog_service import BlogService
from src.services.comment_service import CommentService
from src.services.like_service import LikeService

def main():
    user_service = UserService()
    blog_service = BlogService()
    comment_service = CommentService()
    like_service = LikeService()

    print("Welcome to Blog Nest CLI")
    choice = input("1. Signup  2. Login: ").strip()

    current_user = None
    if choice == "1":
        name = input("Full Name: ").strip()
        email = input("Email: ").strip()
        password = input("Password: ").strip()
        user_service.signup(name, email, password)
        print("✅ User created! Please login to continue.")
        return
    elif choice == "2":
        email = input("Email: ").strip()
        password = input("Password: ").strip()
        user = user_service.login(email, password)
        if not user:
            print("❌ Invalid credentials")
            return
        current_user = user
        print(f"✅ Login successful! Welcome {user['name']}")

    while True:
        print("""
Menu:
1. Create Blog
2. List Blogs
3. Search Blogs
4. Delete Blog
5. Add Comment
6. View Comments
7. Like Blog
8. Count Likes
9. Update Profile
10. Exit
        """)
        option = input("Choose an option: ").strip()

        if option == "1":
            title = input("Blog Title: ").strip()
            content = input("Content: ").strip()
            category = input("Category: ").strip()
            blog_service.create_blog(current_user["id"], title, content, category)
            print("✅ Blog created!")

        elif option == "2":
            blogs = blog_service.list_blogs()
            if not blogs:
                print("ℹ️ No blogs found.")
            else:
                for b in blogs:
                    print(f"{b['id']}. {b['title']} - {b['category']} (by User {b['user_id']})")

        elif option == "3":
            keyword = input("Keyword to search: ").strip()
            blogs = blog_service.search_blogs(keyword)
            if not blogs:
                print("ℹ️ No matching blogs found.")
            else:
                for b in blogs:
                    print(f"{b['id']}. {b['title']} - {b['category']} (by User {b['user_id']})")

        elif option == "4":
            blog_id = int(input("Blog ID to delete: ").strip())
            deleted = blog_service.delete_blog(blog_id)
            print("✅ Blog deleted!" if deleted else "❌ Blog not found.")

        elif option == "5":
            blog_id = int(input("Blog ID to comment on: ").strip())
            comment_text = input("Comment: ").strip()
            comment_service.add_comment(blog_id, current_user["id"], comment_text)
            print("✅ Comment added!")

        elif option == "6":
            blog_id = int(input("Blog ID to view comments: ").strip())
            comments = comment_service.get_comments(blog_id)
            if not comments:
                print("ℹ️ No comments for this blog.")
            else:
                for c in comments:
                    print(f"{c['id']}: {c['comment']} (by User {c['user_id']})")

        elif option == "7":
            blog_id = int(input("Blog ID to like: ").strip())
            like_service.like_blog(blog_id, current_user["id"])
            print("👍 Blog liked!")

        elif option == "8":
            blog_id = int(input("Blog ID to count likes: ").strip())
            print(f"Total Likes: {like_service.count_likes(blog_id)}")

        elif option == "9":
            new_name = input("New Name (leave blank to skip): ").strip()
            new_password = input("New Password (leave blank to skip): ").strip()
            user_service.update_profile(current_user["id"], new_name or None, new_password or None)
            print("✅ Profile updated!")

        elif option == "10":
            print("👋 Exiting. Goodbye!")
            break

        else:
            print("⚠️ Invalid option. Please try again.")

if __name__ == "__main__":
    main()
