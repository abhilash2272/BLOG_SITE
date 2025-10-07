import streamlit as st
from src.services.user_service import UserService
from src.services.blog_service import BlogService
from src.services.comment_service import CommentService
from src.services.like_service import LikeService

# Initialize services
user_service = UserService()
blog_service = BlogService()
comment_service = CommentService()
like_service = LikeService()

# Session state
if "user" not in st.session_state:
    st.session_state.user = None

# --- Authentication ---
if st.session_state.user is None:
    st.title("BlogNest - Login / Signup")
    auth_option = st.radio("Choose:", ["Login", "Signup"], horizontal=True)

    if auth_option == "Signup":
        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Signup"):
            user_service.signup(name, email, password)
            st.success("✅ User created! Login now.")
    else:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user = user_service.login(email, password)
            if user:
                st.session_state.user = user
                st.success(f"✅ Welcome {user['name']}!")
            else:
                st.error("❌ Invalid credentials")

# --- Main Blog Features ---
if st.session_state.user:
    st.sidebar.title(f"Welcome, {st.session_state.user['name']}!")
    menu = ["Create Blog", "List Blogs", "Search Blogs", "Delete Blog",
            "Add Comment", "View Comments", "Like Blog", "Count Likes",
            "Update Profile", "Logout"]
    choice = st.sidebar.selectbox("Menu", menu)

    user_id = st.session_state.user["id"]

    if choice == "Create Blog":
        st.subheader("Create a New Blog")
        title = st.text_input("Title")
        content = st.text_area("Content")
        category = st.text_input("Category")
        if st.button("Create"):
            blog_service.create_blog(user_id, title, content, category)
            st.success("✅ Blog created!")

    elif choice == "List Blogs":
        st.subheader("All Blogs")
        blogs = blog_service.list_blogs()
        if blogs:
            for b in blogs:
                with st.container():
                    st.markdown(f"### {b['title']}")
                    st.markdown(f"**Category:** {b['category']}  |  **Author:** User {b['user_id']}  |  **Blog ID:** {b['id']}")
                    st.markdown(f"{b['content'][:200]}{'...' if len(b['content'])>200 else ''}")
                    comments = comment_service.get_comments(b["id"])
                    likes_count = like_service.count_likes(b["id"])
                    st.markdown(f"💬 Comments: {len(comments)}  |  ❤️ Likes: {likes_count}")
                    st.divider()
        else:
            st.info("No blogs found.")

    elif choice == "Search Blogs":
        keyword = st.text_input("Enter keyword to search")
        if st.button("Search"):
            results = blog_service.search_blogs(keyword)
            if results:
                for b in results:
                    with st.container():
                        st.markdown(f"### {b['title']}")
                        st.markdown(f"**Category:** {b['category']}  |  **Author:** User {b['user_id']}  |  **Blog ID:** {b['id']}")
                        st.markdown(f"{b['content'][:200]}{'...' if len(b['content'])>200 else ''}")
                        comments = comment_service.get_comments(b["id"])
                        likes_count = like_service.count_likes(b["id"])
                        st.markdown(f"💬 Comments: {len(comments)}  |  ❤️ Likes: {likes_count}")
                        st.divider()
            else:
                st.info("No blogs found with this keyword.")

    elif choice == "Delete Blog":
        blog_id = st.number_input("Enter blog ID to delete", min_value=1, step=1)
        if st.button("Delete"):
            res = blog_service.delete_blog(blog_id)
            st.success(res.get("message", "❌ Error"))

    elif choice == "Add Comment":
        blog_id = st.number_input("Blog ID", min_value=1, step=1)
        comment_text = st.text_area("Comment")
        if st.button("Add Comment"):
            comment_service.add_comment(blog_id, user_id, comment_text)
            st.success("✅ Comment added!")

    elif choice == "View Comments":
        blog_id = st.number_input("Blog ID to view comments", min_value=1, step=1)
        if st.button("View Comments"):
            comments = comment_service.get_comments(blog_id)
            if comments:
                for c in comments:
                    st.markdown(f"**User {c['user_id']}:** {c['comment']}")
                    st.divider()
            else:
                st.info("No comments yet.")

    elif choice == "Like Blog":
        blog_id = st.number_input("Blog ID to like", min_value=1, step=1)
        if st.button("Like"):
            like_service.like_blog(blog_id, user_id)
            st.success("✅ Liked!")

    elif choice == "Count Likes":
        blog_id = st.number_input("Blog ID to count likes", min_value=1, step=1)
        if st.button("Show Likes"):
            st.write(f"Total Likes: {like_service.count_likes(blog_id)}")

    elif choice == "Update Profile":
        new_name = st.text_input("New Name", value=st.session_state.user["name"])
        new_password = st.text_input("New Password", type="password")
        if st.button("Update"):
            user_service.update_profile(user_id, new_name, new_password)
            st.success("✅ Profile updated!")
            st.session_state.user["name"] = new_name

    elif choice == "Logout":
        st.session_state.user = None
        st.experimental_rerun()
