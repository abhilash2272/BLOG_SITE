from supabase import create_client
import os
import streamlit as st
#from dotenv import load_dotenv

#load_dotenv()

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
