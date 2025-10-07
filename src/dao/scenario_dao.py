from src.supabase_config import supabase

def add_scenario(user_id, description):
    res = supabase.table("scenarios").insert({"user_id": user_id, "description": description}).execute()
    return getattr(res, "data", None)

def get_all_scenarios():
    res = supabase.table("scenarios").select("*").execute()
    return getattr(res, "data", [])
