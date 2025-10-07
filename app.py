import streamlit as st
from src.services.user_service import UserService
from src.services.blog_service import BlogService

user_service = UserService()
blog_service = BlogService()

if "user" not in st.session_state:
    st.session_state.user = None

# --- Authentication ---
if st.session_state.user is None:
    st.title("Blog Nest - Login / Signup")
    auth_option = st.radio("Choose:", ["Login", "Signup"])

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
    st.title(f"Welcome to Blog Nest, {st.session_state.user['name']}")
    menu = ["Create Blog", "List Blogs", "Search Blogs", "Delete Blog", "Update Profile", "Logout"]
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
                st.write(f"**ID:** {b['id']}\n**Title:** {b['title']}\n**Content:** {b['content']}\n**Category:** {b['category']}\n**User ID:** {b['user_id']}\n---")
        else:
            st.info("No blogs found.")

    elif choice == "Search Blogs":
        keyword = st.text_input("Enter keyword")
        if st.button("Search"):
            results = blog_service.search_blogs(keyword)
            if results:
                for b in results:
                    st.write(f"**ID:** {b['id']}\n**Title:** {b['title']}\n**Content:** {b['content']}\n**Category:** {b['category']}\n**User ID:** {b['user_id']}\n---")
            else:
                st.info("No blogs found with this keyword.")

    elif choice == "Delete Blog":
        blog_id = st.number_input("Enter blog ID to delete", min_value=1, step=1)
        if st.button("Delete"):
            res = blog_service.delete_blog(blog_id)
            st.success(res.get("message"))

    elif choice == "Update Profile":
        new_name = st.text_input("New Name", value=st.session_state.user["name"])
        new_password = st.text_input("New Password", type="password")
        if st.button("Update"):
            user_service.update_profile(user_id, new_name, new_password)
            st.session_state.user["name"] = new_name
            st.success("✅ Profile updated!")

    elif choice == "Logout":
        st.session_state.user = None
        st.experimental_rerun()
