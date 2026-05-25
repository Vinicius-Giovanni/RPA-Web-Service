from supabase import create_client, Client
import os

from settings.paths import ENV_PATH
from dotenv import load_dotenv

load_dotenv(dotenv_path=ENV_PATH)

SUPABASE_URL = os.getenv("API_URL")
SUPABASE_KEY = os.getenv("API_KEY_ANON_PUBLIC")
SUPABASE_JWT = os.getenv("JWT_SECRET")
SUPABASE_JWKS_URL = os.getenv("JWKS_URL")

if not all([SUPABASE_URL, SUPABASE_KEY, SUPABASE_JWT]):
    raise EnvironmentError("One or more Supabase environment variables are missing")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)