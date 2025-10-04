import streamlit as st
from src.services.user_service import UserService
from src.services.blog_service import BlogService
from src.services.comment_service import CommentService
from src.services.like_service import LikeService

user_service = UserService()
blog_service = BlogService()
comment_service = CommentService()
like_service = LikeService()

st.set_page_config(page_title="Blog Nest", layout="wide")

# Session state
if "user" not in st.session_state:
    st.session_state.user = None

st.title("📝 Blog Nest")

if not st.session_state.user:
    choice = st.sidebar.radio("Login / Signup", ["Login", "Signup"])
    if choice == "Signup":
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Signup"):
            if name and email and password:
                user_service.signup(name, email, password)
                st.success("✅ User created! Please login.")
    else:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user = user_service.login(email, password)
            if user:
                st.session_state.user = user
                st.success(f"✅ Welcome {user['name']}")
                st.experimental_rerun()
            else:
                st.error("❌ Invalid credentials")
else:
    st.sidebar.success(f"Logged in as {st.session_state.user['name']}")
    menu = st.sidebar.radio("Menu", ["Create Blog", "View Blogs", "Search Blogs", "Profile", "Logout"])

    if menu == "Create Blog":
        st.subheader("✍️ Create Blog")
        title = st.text_input("Title")
        content = st.text_area("Content")
        category = st.text_input("Category")
        if st.button("Publish"):
            blog_service.create_blog(st.session_state.user["id"], title, content, category)
            st.success("✅ Blog published!")

    elif menu == "View Blogs":
        st.subheader("📚 All Blogs")
        blogs = blog_service.list_blogs()
        if blogs:
            for b in blogs:
                st.markdown(f"### {b['title']} ({b['category']})")
                st.write(b["content"])
                st.caption(f"By User {b['user_id']}")
                if st.button(f"👍 Like {b['id']}"):
                    like_service.like_blog(b["id"], st.session_state.user["id"])
                st.text(f"Likes: {like_service.count_likes(b['id'])}")

                comments = comment_service.get_comments(b["id"])
                with st.expander("💬 Comments"):
                    for c in comments:
                        st.write(f"- {c['comment']} (User {c['user_id']})")
                    new_comment = st.text_input(f"Add comment for blog {b['id']}")
                    if st.button(f"Comment {b['id']}"):
                        comment_service.add_comment(b["id"], st.session_state.user["id"], new_comment)
                        st.success("✅ Comment added!")

    elif menu == "Search Blogs":
        st.subheader("🔍 Search Blogs")
        keyword = st.text_input("Enter keyword")
        if st.button("Search"):
            blogs = blog_service.search_blogs(keyword)
            if blogs:
                for b in blogs:
                    st.write(f"**{b['title']}** - {b['category']}")
            else:
                st.info("No matching blogs found.")

    elif menu == "Profile":
        st.subheader("👤 Update Profile")
        new_name = st.text_input("New Name")
        new_password = st.text_input("New Password", type="password")
        if st.button("Update"):
            user_service.update_profile(st.session_state.user["id"], new_name or None, new_password or None)
            st.success("✅ Profile updated!")

    elif menu == "Logout":
        st.session_state.user = None
        st.experimental_rerun()
