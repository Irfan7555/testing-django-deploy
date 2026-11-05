from supabase_client import supabase

try:
    response = supabase.table("tasks").select("*").limit(1).execute()

    print("Supabase connected successfully!")
    print(response.data)

except Exception as e:
    print("Connection failed:", e)