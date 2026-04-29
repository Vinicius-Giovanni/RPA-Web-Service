from settings.paths import ENV_PATH

from dotenv import load_dotenv
from supabase import create_client, Client

import os
from datetime import datetime, timezone

load_dotenv(dotenv_path=ENV_PATH)

api_url: str = os.getenv("API_URL")
api_keys_anon_public: str = os.getenv("API_KEYS_ANON_PUBLIC")

supabase: Client = create_client(api_url, api_keys_anon_public)

# Test connection by fetching a single row from the 'posts' table
try:
    test = supabase.table("posts").select("id").limit(1).execute()
    print("Connection successfull Sample data:", test.data)
except Exception as e:
    print("Connection to Supabase failed:", e)


# Sending data to the 'posts' table
try:
    data = {
        "title": "My firts Supabase post",
        "content": "This is my very firts post using Supabase and Python!",
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    response = supabase.table("posts").insert(data).execute()
    print("Insert successfull New row:", response.data)
except Exception as e:
    print("Failed to insert data:", e)

# Returning the data from table
try:
    response = supabase.table("posts").select("id").limit(1).execute()
    print("Connection successfull! Sample data:", test.data)
except Exception as e:
    print("Failed to fetch data:", e)