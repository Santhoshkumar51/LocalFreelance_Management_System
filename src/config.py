import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load .env file for local development
load_dotenv()

def get_supabase() -> Client:
    # Try Streamlit secrets first (for deployment), then fall back to environment variables (for local)
    try:
        import streamlit as st
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
    except:
        # Fall back to .env file
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        raise ValueError("Supabase credentials not found. Set SUPABASE_URL and SUPABASE_KEY")
    
    return create_client(url, key)