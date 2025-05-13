from supabase import create_client
import os
from dotenv import load_dotenv
load_dotenv()

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def get_user_by_whatsapp(wa_id):
    res = supabase.table("users").select("*").eq("whatsapp", wa_id).execute()
    return res.data[0] if res.data else None

def get_pending_user(wa_id):
    res = supabase.table("cadastros_pendentes").select("*").eq("whatsapp", wa_id).execute()
    return res.data[0] if res.data else None
