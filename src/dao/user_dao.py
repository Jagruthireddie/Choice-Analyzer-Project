from src.supabase_config import supabase

def create_user(name, email, password, role="user"):
    res = supabase.table("users").insert({"name": name, "email": email, "password": password, "role": role}).execute()
    return getattr(res, "data", None)

def get_user_by_email(email):
    res = supabase.table("users").select("*").eq("email", email).maybe_single().execute()
    return getattr(res, "data", None)
