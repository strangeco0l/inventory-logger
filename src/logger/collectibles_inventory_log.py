from logger.models import Collectibles
from .supabase_client import supabase


def save_collectibles_to_supabase(collectibles):
    data = {
        "user_id": collectibles.user_id,
        "purchase_date": collectibles.purchase_date,
        "retailer": collectibles.retailer,
        "release_date": collectibles.release_date,
        "brand": collectibles.brand,
        "item": collectibles.item,
        "variation": collectibles.variation,
        "retail_price": collectibles.retail_price,
        "resale_price": collectibles.resale_price,
        "quantity": collectibles.quantity,
        "profit_per": collectibles.profit_per,
        "profit": collectibles.profit
    }
    supabase.table("collectibles").insert(data).execute()


def get_validated_input(prompt, cast_type=str, allow_empty=False):
    while True:
        value = input(prompt).strip()
        if not value and not allow_empty:
            print("Input cannot be empty.")
            continue
        try:
            return cast_type(value)
        except ValueError:
            print(f"Invalid input. Please enter a valid {cast_type.__name__}.")


def gather_collectibles_data(user_id):
    print("\n--- Enter Collectible Info ---")
    collectibles = Collectibles(
        user_id=user_id,
        release_date=get_validated_input("Release date?: "),
        purchase_date=get_validated_input("Purchase date?: "),
        retailer=get_validated_input("Retailer?: ").title(),
        brand=get_validated_input("Brand?: ").title(),
        item=get_validated_input("Item?: ").title(),
        variation=get_validated_input("Variation?: ")
    )

    save_collectibles_to_supabase(collectibles)
    print("✅ Collectible logged successfully!\n")


def collectibles_inventory_log(user_id):
    print("🧸 Collectibles Inventory Logger Started\n")
    while True:
        gather_collectibles_data(user_id)
        user_input = input("Log another collectible? (y/n): ").strip().lower()
        if user_input == 'n':
            print("📦 Exiting Collectibles Inventory Log.\n")
            break
