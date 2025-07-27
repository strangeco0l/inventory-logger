from logger.models import Media
from logger.data_handling import save_media_data
from .supabase_client import supabase


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


def gather_media_data():
    print("\n--- Enter Media Info ---")
    purchase_date = get_validated_input("Purchase date?: ")
    retailer = get_validated_input("Retailer?: ").title()

    media_type = get_validated_input("Media type (Vinyl or CD)?: ", str, valid_values=['vinyl', 'cd'])
    speed = get_validated_input("Vinyl speed?: ") if media_type.lower() == 'vinyl' else "N/A"

    artist = get_validated_input("Artist?: ")
    album = get_validated_input("Album?: ")
    variation = get_validated_input("Variation?: ")
    signed = get_validated_input("Signed?: ")
    edition = get_validated_input("Edition?: ")
    quantity = get_validated_input("Quantity?: ", int)
    retail_price = get_validated_input("What did you pay?: $", float)
    resale_price = get_validated_input("What's it worth?: $", float)

    media = Media(
        purchase_date=purchase_date,
        retailer=retailer,
        media=media_type.title(),
        speed=speed,
        artist=artist,
        album=album,
        variation=variation,
        signed=signed,
        edition=edition,
        retail_price=retail_price,
        resale_price=resale_price,
        quantity=quantity
    )

    save_media_data(media)
    print("✅ Media logged successfully!\n")

    return media  # <-- add this line



def media_inventory_log():
    print("📀 Media Inventory Logger Started\n")
    while True:
        gather_media_data()
        user_input = input("Log another media item? (y/n): ").strip().lower()
        if user_input == 'n':
            print("🛑 Exiting Media Inventory Log.\n")
            break


def save_media_to_supabase(media):
    data = {
        "purchase_date": media.purchase_date,
        "retailer": media.retailer,
        "media_type": media.media_type,  # "Vinyl" or "CD"
        "speed": media.speed,            # "33 1/3", "45", etc.
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

