from src.supabase_config import supabase

def add_review(scenario_id, positive_advice, negative_advice, admin_id):
    data = {
        "scenario_id": scenario_id,
        "positive_advice": positive_advice,
        "negative_advice": negative_advice,
        "admin_id": admin_id,
    }
    res = supabase.table("reviews").insert(data).execute()
    return getattr(res, "data", None)

def get_reviews_for_scenario(scenario_id):
    res = supabase.table("reviews").select("*").eq("scenario_id", scenario_id).execute()
    return getattr(res, "data", [])
