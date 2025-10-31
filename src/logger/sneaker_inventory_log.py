import os
import json
from supabase import create_client, Client
from datetime import datetime
from src.logger.models import Sneaker
from src.logger.supabase_client import supabase
from src.logger.ebay_sold_scraper import get_average_sold_price


USER_STATE_FILE = "user_state.json"
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# -------------------------------
# User Sign-In / Saved State
# -------------------------------
def save_user_state(user_id, email):
    with open(USER_STATE_FILE, "w") as f:
        json.dump({"user_id": user_id, "email": email}, f)

def load_user_state():
    if os.path.exists(USER_STATE_FILE):
        with open(USER_STATE_FILE, "r") as f:
            return json.load(f)
    return None

def sign_in():
    email = input("Enter your email: ").strip()
    response = supabase.table("users").select("id").eq("email", email).execute()

    if response.data:
        user_id = response.data[0]["id"]
        print(f"[DEBUG] Found existing user {email} → {user_id}")
    else:
        # Create a new user record if not found
        from uuid import uuid4
        user_id = str(uuid4())
        print(f"[DEBUG] Creating new user {email} → {user_id}")
        supabase.table("users").insert({"id": user_id, "email": email}).execute()

    return user_id


# -------------------------------
# Input Helpers
# -------------------------------


def get_or_create_user(email: str) -> str:
    """
    Check if a user exists; if not, create a new one.
    Returns the user_id (UUID) for the sneaker logger.
    """
    # Check if user exists
    response = supabase.table("users").select("id").eq("email", email).execute()
    if response.data:
        return response.data[0]["id"]

    # Create new user
    new_user_response = supabase.table("users").insert({"email": email}).execute()
    if new_user_response.data:
        return new_user_response.data[0]["id"]

    raise ValueError("Failed to get or create user")


def get_validated_input(prompt, cast_type=str, allow_empty=False):
    while True:
        val = input(prompt).strip()
        if not val and allow_empty:
            return None
        if not val:
            print("Input cannot be empty. Try again.")
            continue
        try:
            return cast_type(val)
        except ValueError:
            print(f"Please enter a valid {cast_type.__name__}.")


def get_date_input(prompt):
    while True:
        val = input(prompt).strip()
        if not val:
            return None
        try:
            datetime.strptime(val, "%Y-%m-%d")
            return val
        except ValueError:
            print("Please enter a valid date in YYYY-MM-DD format, or leave empty.")

# -------------------------------
# Save Sneaker
# -------------------------------


def save_sneaker_to_supabase(sneaker):
    data = {
        "user_id": sneaker.user_id,
        "purchase_date": sneaker.purchase_date,
        "retailer": sneaker.retailer,
        "release_date": sneaker.release_date,
        "size": sneaker.size,
        "brand": sneaker.brand,
        "model": sneaker.model,
        "colorway": sneaker.colorway,
        "sku": sneaker.sku,
        "retail_price": sneaker.retail_price,
        "resale_price": sneaker.resale_price,
        "quantity": sneaker.quantity,
        "profit": sneaker.profit
    }
    supabase.table("sneakers").insert(data).execute()

# -------------------------------
# Gather Sneaker Data
# -------------------------------
def gather_sneaker_data(user_id):
    print("\n--- Enter Sneaker Info ---")

    brand = get_validated_input("Brand?: ").title()
    model = get_validated_input("Model?: ").title()
    colorway = get_validated_input("Colorway?: ").title()
    sku = get_validated_input("SKU?: ")

    retail_price = get_validated_input("Purchase Price?: $", float)
    quantity = get_validated_input("Quantity?: ", int)
    size = get_validated_input("Size?: ")

    # Optional dates
    purchase_date = get_date_input("Purchase date (YYYY-MM-DD)?: ") or None
    release_date = get_date_input("Release date (YYYY-MM-DD)?: ") or None

    # Optional resale price — use eBay scraper if not provided
    resale_price_input = input("Resale Price (leave blank to auto-fetch from eBay): ").strip()
    if resale_price_input:
        resale_price = float(resale_price_input)
    else:
        print("\n🔍 Fetching average sold price from eBay...")
        try:
            search_query = f"{brand} {model} {colorway} {sku}".strip()
            resale_price = get_average_sold_price(search_query)
            if resale_price:
                print(f"✅ Found average resale price: ${resale_price}")
            else:
                print("⚠️ No recent sales found on eBay. Leaving resale price empty.")
                resale_price = None
        except Exception as e:
            print(f"⚠️ eBay scraper failed: {e}")
            resale_price = None

    # Calculate profit safely
    profit_per = round(resale_price - retail_price, 2) if resale_price is not None else None
    total_profit = round(profit_per * quantity, 2) if profit_per is not None else None

    sneaker = Sneaker(
        user_id=user_id,
        purchase_date=purchase_date,
        retailer=get_validated_input("Retailer?: ").title(),
        release_date=release_date,
        size=size,
        brand=brand,
        model=model,
        colorway=colorway,
        sku=sku,
        retail_price=retail_price,
        resale_price=resale_price,
        quantity=quantity,
        profit_per=profit_per,
        profit=total_profit
    )

    save_sneaker_to_supabase(sneaker)
    print(f"✅ Sneaker logged successfully for {brand} {model}!")


# -------------------------------
# Sneaker Logger Loop
# -------------------------------
def sneaker_inventory_log(user_id):
    print("📦 Sneaker Inventory Logger Started\n")
    while True:
        gather_sneaker_data(user_id)
        cont = input("Add another? (y/n): ").strip().lower()
        if cont == "n":
            print("👟 Exiting Sneaker Inventory Log.\n")
            break

# -------------------------------
# Main Entry
# -------------------------------
def main():
    user_id = sign_in()
    if not user_id:
        return

    options = {
        "Sneakers": sneaker_inventory_log,
        # You can add Media and Collectibles here
    }

    while True:
        choice = input(
            "Enter one of the following to log inventory: Sneakers (or type 'exit' to quit): "
        ).strip().title()

        if choice.lower() == "exit":
            print("👋 Goodbye!")
            break

        if choice in options:
            options[choice](user_id)
        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    main()
