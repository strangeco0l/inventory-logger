from logger.models import Collectibles
from logger.data_handling import save_collectibles_data
from .supabase_client import supabase


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


def gather_collectibles_data():
    print("\n--- Enter Collectible Info ---")
    purchase_date = get_validated_input("Purchase date?: ")
    retailer = get_validated_input("Retailer?: ").title()
    brand = get_validated_input("Brand?: ").title()
    item = get_validated_input("Item?: ").title()
    variation = get_validated_input("Variation?: ")
    quantity = get_validated_input("Quantity?: ", int)
    retail_price = get_validated_input("What did you pay?: $", float)
    resale_price = get_validated_input("What's it worth?: $", float)

    collectible = Collectibles(
        purchase_date=purchase_date,
        retailer=retailer,
        brand=brand,
        item=item,
        variation=variation,
        retail_price=retail_price,
        resale_price=resale_price,
        quantity=quantity
    )

    save_collectibles_data(collectible)
    print("✅ Collectible logged successfully!\n")


def collectibles_inventory_log():
    print("🧸 Collectibles Inventory Logger Started\n")
    while True:
        gather_collectibles_data()
        user_input = input("Log another collectible? (y/n): ").strip().lower()
        if user_input == 'n':
            print("📦 Exiting Collectibles Inventory Log.\n")
            break


def save_collectible_to_supabase(collectible):
    data = {
        "purchase_date": collectible.purchase_date,
        "retailer": collectible.retailer,
        "brand": collectible.brand,
        "item": collectible.item,
        "variation": collectible.variation,
        "retail_price": collectible.retail_price,
        "resale_price": collectible.resale_price,
        "quantity": collectible.quantity,
        "profit_per": collectible.profit_per,
        "profit": collectible.profit
    }
    supabase.table("collectibles").insert(data).execute()

