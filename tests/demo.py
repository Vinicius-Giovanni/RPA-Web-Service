from supabase import create_client, Client
import os

from settings.paths import ENV_PATH
from dotenv import load_dotenv

load_dotenv(dotenv_path=ENV_PATH)

# Criando cliente Supabase usando as variáveis de ambientes

SUPABASE_URL= str = os.getenv("API_URL")
SUPABASE_KEY= str = os.getenv("API_KEY_ANON_PUBLIC")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# !Enviando dados para a tabela "user_table"
# new_row = {'full_name': 'john Doe'}
# supabase.table("user_table").insert(new_row).execute()

# !Atualizando dados na tabela "user_table" usando o nome existente como referencia
# new_row = {'full_name': 'jane Doe'}
# supabase.table("user_table").update(new_row).eq("full_name", "john Doe").execute()

# !Removendo dados da tabela "user_table" usando o nome existente como referencia
supabase.table('user_table').delete().eq("full_name", "jane Doe").execute()

# !Puxando dados da tabela "user_table" e imprimindo os resultados
results = supabase.table("user_table").select("*").execute()
print(results)


