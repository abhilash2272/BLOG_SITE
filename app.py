import streamlit as st
from src.services.user_service import UserService
from src.services.blog_service import BlogService
from src.services.comment_service import CommentService
from src.services.like_service import LikeService

# Services
user_service = UserService()
blog_service = BlogService()
comment_service = CommentService()
like_service = LikeService()

# Session State
if "user" not in st.session_state:
    st.session_state.user = None

# --- Authentication ---
if st.session_state.user is None:
    st.title("BlogNest - Login / Signup")
    auth_option = st.radio("Choose:", ["Login", "Signup"])

    if auth_option == "Signup":
        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Signup"):
            try:
                user_service.signup(name, email, password)
                st.success("✅ User created! Login now.")
            except Exception as e:
                st.error(f"❌ {e}")
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
    st.title(f"Welcome to BlogNest, {st.session_state.user['name']}")
    menu = [
        "Create Blog", "List Blogs", "Search Blog by ID", "Delete Blog",
        "Add Comment", "View Comments", "Like Blog", "Count Likes",
        "Update Profile", "Logout"
    ]
    choice = st.sidebar.selectbox("Menu", menu)
    user_id = st.session_state.user["id"]

    # --- Create Blog ---
    if choice == "Create Blog":
        st.subheader("Create a New Blog")
        title = st.text_input("Title")
        content = st.text_area("Content")
        category = st.text_input("Category")
        if st.button("Create"):
            blog_service.create_blog(user_id, title, content, category)
            st.success("✅ Blog created!")

    # --- List Blogs ---
    elif choice == "List Blogs":
        st.subheader("All Blogs")
        blogs = blog_service.list_blogs()
        if blogs:
            num_cols = 2
            for i in range(0, len(blogs), num_cols):
                cols = st.columns(num_cols)
                for j, b in enumerate(blogs[i:i+num_cols]):
                    with cols[j]:
                        st.markdown(
                            f"""
                            <div style="border:1px solid #e0e0e0; padding:15px; border-radius:10px; background-color:#f9f9f9;">
                                <h3 style="color:#2c3e50;">{b['title']}</h3>
                                <p><strong>Category:</strong> <span style="color:#3498db;">{b['category']}</span> | 
                                <strong>Author:</strong> User {b['user_id']} | <strong>Blog ID:</strong> {b['id']}</p>
                                <p>{b['content'][:150]}{'...' if len(b['content'])>150 else ''}</p>
                                <p>💬 Comments: {len(comment_service.get_comments(b['id']))} | ❤️ Likes: {like_service.count_likes(b['id'])}</p>
                            </div>
                            """, unsafe_allow_html=True
                        )
        else:
            st.info("No blogs found.")

    # --- Search Blog by ID ---
    elif choice == "Search Blog by ID":
        blog_id = st.number_input("Enter Blog ID", min_value=1, step=1)
        if st.button("Search"):
            blog = blog_service.get_blog_by_id(blog_id)
            if blog:
                st.markdown(
                    f"""
                    <div style="border:1px solid #e0e0e0; padding:15px; border-radius:10px; background-color:#f9f9f9;">
                        <h3 style="color:#2c3e50;">{blog['title']}</h3>
                        <p><strong>Category:</strong> <span style="color:#3498db;">{blog['category']}</span> | 
                        <strong>Author:</strong> User {blog['user_id']} | <strong>Blog ID:</strong> {blog['id']}</p>
                        <p>{blog['content']}</p>
                        <p>💬 Comments: {len(comment_service.get_comments(blog['id']))} | ❤️ Likes: {like_service.count_likes(blog['id'])}</p>
                    </div>
                    """, unsafe_allow_html=True
                )
            else:
                st.info("No blog found with this ID.")

    # --- Delete Blog ---
    elif choice == "Delete Blog":
        blog_id = st.number_input("Enter blog ID to delete", min_value=1, step=1)
        if st.button("Delete"):
            res = blog_service.delete_blog(blog_id)
            st.success(res.get("message"))

    # --- Add Comment ---
    elif choice == "Add Comment":
        blog_id = st.number_input("Blog ID", min_value=1, step=1)
        comment_text = st.text_area("Comment")
        if st.button("Add Comment"):
            try:
                comment_service.add_comment(blog_id, user_id, comment_text)
                st.success("✅ Comment added!")
            except Exception as e:
                st.error(f"❌ {e}")

    # --- View Comments ---
    elif choice == "View Comments":
        blog_id = st.number_input("Blog ID", min_value=1, step=1)
        if st.button("View Comments"):
            comments = comment_service.get_comments(blog_id)
            if comments:
                for c in comments:
                    user = user_service.get_user_by_id(c["user_id"])
                    st.write(f"**{user['name']}**: {c['comment']}")
            else:
                st.info("No comments yet.")

    # --- Like Blog ---
    elif choice == "Like Blog":
        blog_id = st.number_input("Blog ID", min_value=1, step=1)
        if st.button("Like"):
            try:
                like_service.like_blog(blog_id, user_id)
                st.success("✅ Liked!")
            except Exception as e:
                st.error(f"❌ {e}")  # Already liked

    # --- Count Likes ---
    elif choice == "Count Likes":
        blog_id = st.number_input("Blog ID", min_value=1, step=1)
        if st.button("Show Likes"):
            st.write(f"Total Likes: {like_service.count_likes(blog_id)}")

    # --- Update Profile ---
    elif choice == "Update Profile":
        new_name = st.text_input("New Name", value=st.session_state.user["name"])
        new_password = st.text_input("New Password", type="password")
        if st.button("Update"):
            user_service.update_profile(user_id, new_name, new_password)
            st.success("✅ Profile updated!")
            st.session_state.user["name"] = new_name

    # --- Logout ---
    elif choice == "Logout":
        st.session_state.user = None
        st.experimental_rerun()
