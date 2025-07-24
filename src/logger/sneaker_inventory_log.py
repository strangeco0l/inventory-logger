from dataclasses import dataclass, field
from data_handling import save_sneaker_data  # Import at top

@dataclass
class Sneaker:
    purchase_date: str
    retailer: str
    release_date: str
    size: str
    brand: str
    model: str
    colorway: str
    sku: str
    retail_price: float
    resale_price: float
    quantity: int = 1
    profit_per: float = field(init=False)
    profit: float = field(init=False)

    def __post_init__(self):
        self.profit_per = self.resale_price - self.retail_price
        self.profit = self.profit_per * self.quantity


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


def gather_sneaker_data():
    print("\n--- Enter Sneaker Info ---")
    sneaker = Sneaker(
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

    save_sneaker_data(sneaker)
    print("✅ Sneaker logged successfully!\n")


def sneaker_inventory_log():
    print("📦 Sneaker Inventory Logger Started\n")
    while True:
        gather_sneaker_data()

        user_input = input("Add another? (y/n): ").strip().lower()
        if user_input == 'n':
            print("👟 Exiting Sneaker Inventory Log.\n")
            break
