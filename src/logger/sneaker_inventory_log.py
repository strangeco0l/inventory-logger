from logger.data_handling import save_sneaker_data
from logger.models import Sneaker
from .supabase_client import supabase


def save_sneaker_to_supabase(sneaker):
    data = {
        "user_id": sneaker.user_id,  # <-- Include user_id here
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
        "profit_per": sneaker.profit_per,
        "profit": sneaker.profit
    }
    supabase.table("sneakers").insert(data).execute()


def get_validated_input(prompt, cast_type=str, allow_empty=False):
    while True:
        user_input = input(prompt).strip()
        if not user_input and not allow_empty:
            print("Input cannot be empty. Please try again.")
            continue
        try:
            return cast_type(user_input)
        except ValueError:
            print(f"Please enter a valid {cast_type.__name__}.")


def gather_sneaker_data(user_id):
    print("\n--- Enter Sneaker Info ---")
    sneaker = Sneaker(
        user_id=user_id,
        purchase_date=get_validated_input("Purchase date?: "),
        retailer=get_validated_input("Retailer?: ").title(),
        release_date=get_validated_input("Release date?: "),
        size=get_validated_input("What size?: "),
        brand=get_validated_input("Brand?: ").title(),
        model=get_validated_input("Model?: ").title(),
        colorway=get_validated_input("CW?: ").title(),
        sku=get_validated_input("SKU?: "),
        retail_price=get_validated_input("What did you pay?: $", float),
        resale_price=get_validated_input("What's it worth?: $", float),
        quantity=get_validated_input("Quantity?: ", int)
    )

    save_sneaker_to_supabase(sneaker)  # pass user_id here
    print("✅ Sneaker logged successfully!\n")


def sneaker_inventory_log(user_id):
    print("📦 Sneaker Inventory Logger Started\n")
    while True:
        gather_sneaker_data(user_id)

        user_input = input("Add another? (y/n): ").strip().lower()
        if user_input == 'n':
            print("👟 Exiting Sneaker Inventory Log.\n")
            break



