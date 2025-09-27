import streamlit as st
from supabase import create_client

def get_supabase_client():
    """Initialize Supabase client once and store in session state."""
    if "supabase" not in st.session_state:
        SUPABASE_URL = st.secrets["SUPABASE_URL"]
        SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
        st.session_state.supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    return st.session_state.supabase
