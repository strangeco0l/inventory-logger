from dataclasses import dataclass, field

@dataclass
class Media:
    purchase_date: str
    retailer: str
    media: str
    speed: str
    artist: str
    album: str
    variation: str
    signed: str
    edition: str
    retail_price: float
    resale_price: float
    quantity: int = 1
    profit_per: float = field(init=False)
    profit: float = field(init=False)

    def __post_init__(self):
        # Calculate profit after the object is initialized
        self.profit_per = self.resale_price - self.retail_price
        self.profit = self.profit_per * self.quantity


def media_inventory_log():
    purchase_date = input("Purchase date?: ")
    retailer = input("Retailer?: ")
    # Collecting inputs from the user
    media = input("Media type (Vinyl or CD)?: ")

    # Initialize speed variable
    speed = None

    # Conditional logic based on media type
    if media.lower() == 'vinyl':
        speed = input("Vinyl speed?: ")
    elif media.lower() == 'cd':
        print("Skipping speed input for CD.")
    else:
        print("Invalid media type")
        return  # Exit the function if the media type is not recognized

    artist = input("Artist?: ")
    album = input("Album?: ")
    variation = input("Variation?: ")
    signed = input("Signed?: ")
    edition = input("Edition?: ")
    quantity = int(input("Quantity?: "))
    retail = int(input("What did you pay?: "))
    resale = int(input("Whats it worth?: "))

    # Creating an instance of the Media data class
    media = Media(
        purchase_date=purchase_date,
        retailer=retailer.title(),
        media=media,
        speed=speed,
        artist=artist,
        album=album,
        variation=variation,
        signed=signed,
        edition=edition,
        retail_price=retail,
        resale_price=resale,
        quantity=quantity,
    )

    from data_handling import save_media_data
    save_media_data(media)

