from logger.models import Media
from .supabase_client import supabase


def save_media_to_supabase(media):
    data = {
        "user_id": media.user_id,  # ✅ Ensures this is included
        "purchase_date": media.purchase_date,
        "retailer": media.retailer,
        "media_type": media.media_type,  # Vinyl or CD
        "speed": media.speed,
        "artist": media.artist,
        "album": media.album,
        "variation": media.variation,
        "signed": media.signed,
        "edition": media.edition,
        "retail_price": media.retail_price,
        "resale_price": media.resale_price,
        "quantity": media.quantity,
        "profit_per": media.profit_per,
        "profit": media.profit
    }
    supabase.table("media").insert(data).execute()


def get_validated_input(prompt, cast_type=str, allow_empty=False, valid_values=None):
    while True:
        value = input(prompt).strip()
        if not value and not allow_empty:
            print("Input cannot be empty.")
            continue
        try:
            value = cast_type(value)
            if valid_values and value.lower() not in [v.lower() for v in valid_values]:
                print(f"Invalid input. Expected one of: {', '.join(valid_values)}")
                continue
            return value
        except ValueError:
            print(f"Please enter a valid {cast_type.__name__}.")


def gather_media_data(user_id):
    print("\n--- Enter Media Info ---")
    media = Media(
        user_id=user_id,  # ✅ This is the key fix!
        purchase_date=get_validated_input("Purchase date?: "),
        retailer=get_validated_input("Retailer?: ").title(),
        media_type=get_validated_input("Media type?: "),
        speed=get_validated_input("Speed?: "),
        artist=get_validated_input("Artist?: "),
        album=get_validated_input("Album?: ").title(),
        variation=get_validated_input("Variation?: ").title(),
        signed=get_validated_input("Signed?: ").title(),
        edition=get_validated_input("Edition?: ").title(),

    )

    save_media_to_supabase(media)
    print("✅ Media logged successfully!\n")


def media_inventory_log(user_id):
    print("📀 Media Inventory Logger Started\n")
    while True:
        gather_media_data(user_id)

        user_input = input("Log another media item? (y/n): ").strip().lower()
        if user_input == 'n':
            print("🛑 Exiting Media Inventory Log.\n")
            break
