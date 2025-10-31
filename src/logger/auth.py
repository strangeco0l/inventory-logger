from .supabase_client import supabase


def get_or_create_user(email: str) -> str:
    response = supabase.table("users").select("id").eq("email", email).execute()
    if response.data:
        return response.data[0]["id"]

    new_user_response = supabase.table("users").insert({"email": email}).execute()
    if new_user_response.data:
        return new_user_response.data[0]["id"]

    raise ValueError("Failed to get or create user")
