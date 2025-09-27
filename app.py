import streamlit as st
from src.services.user_service import UserService
from src.services.blog_service import BlogService
from src.services.comment_service import CommentService
from src.services.like_service import LikeService
from src.config import get_supabase_client

# Initialize services with lazy supabase
supabase = get_supabase_client()
user_service = UserService()
blog_service = BlogService()
comment_service = CommentService()
like_service = LikeService()

# Session state
if "user" not in st.session_state:
    st.session_state.user = None

# --- Custom CSS ---
st.markdown("""
<style>
body { background-color: #f7f8fa; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
[data-testid="stSidebar"] { background-color: #ffffff; padding: 2rem 1rem; border-right: 1px solid #e0e0e0; }
.stButton button { background-color: #1a73e8; color: white; border-radius: 6px; padding: 0.5rem 1rem; border: none; font-weight: 600; }
.stButton button:hover { background-color: #155ab6; }
.blog-card { background-color: #ffffff; padding: 1rem; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.06); margin-bottom: 1rem; }
.blog-title { font-size: 1.3rem; font-weight: 700; color: #1a73e8; margin-bottom: 0.2rem; }
.blog-category { font-size: 0.85rem; color: #555; }
.blog-author { font-size: 0.8rem; color: #999; }
.comment-box { margin-top: 0.5rem; background-color: #f1f3f4; padding: 0.5rem; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

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
        user = user_service.signup(name, email, password)
        if user:
            st.success("✅ Account created! Please login.")
        else:
            st.error("⚠️ User already exists.")

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
                if title and content:
                    blog_service.create_blog(st.session_state.user["id"], title, content, category)
                    st.success("🚀 Blog published!")
                    st.experimental_rerun()  # refresh list

        # Read Blogs
        with tab2:
            blogs = blog_service.list_blogs()
            if not blogs:
                st.info("No blogs available. Start writing your first one!")
            else:
                for b in blogs:
                    st.markdown(f"""
                    <div class="blog-card">
                        <div class="blog-title">{b['title']}</div>
                        <div class="blog-category">{b['category']}</div>
                        <div class="blog-author">By User {b['user_id']}</div>
                        <p>{b['content']}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    if st.button(f"👍 Like ({like_service.count_likes(b['id'])})", key=f"like{b['id']}"):
                        like_service.like_blog(b["id"], st.session_state.user["id"])
                        st.experimental_rerun()

                    with st.expander("💬 Comments"):
                        comments = comment_service.get_comments(b["id"])
                        for c in comments:
                            st.markdown(f"<div class='comment-box'>- {c['comment']} (by User {c['user_id']})</div>", unsafe_allow_html=True)
                        new_comment = st.text_input(f"Add a comment", key=f"c{b['id']}")
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
    
