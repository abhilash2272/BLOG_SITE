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

# Initialize session state
if "user" not in st.session_state:
    st.session_state.user = None

# Sidebar Navigation
st.sidebar.title("📖 BlogNest")
menu = ["Signup", "Login", "Blogs", "Profile", "Logout"]
choice = st.sidebar.radio("Navigation", menu)

# --- Signup ---
if choice == "Signup":
    st.header("📝 Signup")
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Create Account"):
        try:
            user = user_service.signup(name, email, password)
            st.success("✅ Account created! Please login.")
        except Exception as e:
            st.error(f"⚠️ {e}")

# --- Login ---
elif choice == "Login":
    st.header("🔑 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = user_service.login(email, password)
        if user:
            st.session_state.user = user
            st.success(f"Welcome {user['name']}! 🎉")
        else:
            st.error("Invalid credentials.")

# --- Blogs ---
elif choice == "Blogs":
    st.header("📚 Blogs")
    if not st.session_state.user:
        st.warning("⚠️ Please login first.")
    else:
        tab1, tab2 = st.tabs(["✍️ Write Blog", "📖 Read Blogs"])

        # Write Blog
        with tab1:
            title = st.text_input("Title")
            content = st.text_area("Content")
            category = st.text_input("Category")
            if st.button("Publish Blog"):
                if title.strip() and content.strip():
                    blog_service.create_blog(st.session_state.user["id"], title, content, category)
                    st.success("🚀 Blog published!")
                else:
                    st.error("⚠️ Title and content cannot be empty.")

        # Read Blogs
        with tab2:
            blogs = blog_service.list_blogs()
            if not blogs:
                st.info("No blogs available. Start writing your first one!")
            else:
                for b in blogs:
                    st.markdown(f"### {b['title']} ({b['category']})")
                    st.markdown(f"By User {b['user_id']}")
                    st.write(b['content'])
                    
                    # Likes & Comments
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        if st.button(f"👍 Like ({like_service.count_likes(b['id'])})", key=f"like{b['id']}"):
                            like_service.like_blog(b["id"], st.session_state.user["id"])
                            st.experimental_rerun()
                    with col2.expander("💬 Comments"):
                        comments = comment_service.get_comments(b["id"])
                        for c in comments:
                            st.markdown(f"- {c['comment']} (by User {c['user_id']})")
                        new_comment = st.text_input("Add a comment", key=f"c{b['id']}")
                        if st.button("Post Comment", key=f"pc{b['id']}") and new_comment.strip():
                            comment_service.add_comment(b["id"], st.session_state.user["id"], new_comment)
                            st.experimental_rerun()

# --- Profile ---
elif choice == "Profile":
    if not st.session_state.user:
        st.warning("⚠️ Please login first.")
    else:
        st.header("👤 Profile")
        new_name = st.text_input("New Name")
        new_password = st.text_input("New Password", type="password")
        if st.button("Update Profile"):
            user_service.update_profile(st.session_state.user["id"], new_name, new_password)
            st.success("✅ Profile updated!")

# --- Logout ---
elif choice == "Logout":
    st.session_state.user = None
    st.info("You have been logged out.")
