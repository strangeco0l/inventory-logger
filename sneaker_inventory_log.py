from dataclasses import dataclass, field

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
        # Calculate profit after the object is initialized
        self.profit_per = self.resale_price - self.retail_price
        self.profit = self.profit_per * self.quantity


def sneaker_inventory_log():
    # function to gather sneaker data
    def gather_sneaker_data():
        purchase_date = input("Purchase date?: ")
        retailer = input("Retailer?: ")
        release_date = input("Release date?: ")
        size = input("What size?: ")
        brand = input("Brand?: ")
        model = input("Model?: ")
        color_way = input("CW?: ")
        sku = input("Sku?: ")
        retail = float(input("What did you pay?: "))
        resale = float(input("Whats it worth?: "))
        quantity = int(input("Quantity?: "))

        # Creating an instance of the Sneaker data class
        sneaker = Sneaker(
            purchase_date=purchase_date,
            retailer=retailer.title(),
            release_date=release_date,
            size=size,
            brand=brand.title(),
            model=model.title(),
            colorway=color_way.title(),
            sku=sku,
            retail_price=retail,
            resale_price=resale,
            quantity=quantity
        )

        # Save the sneaker data
        from data_handling import save_sneaker_data
        save_sneaker_data(sneaker)

        print("Sneaker logged succesfully!\n")
    # Collect the first set of information outside the loop
    gather_sneaker_data()

    # Now enter the loop to log additional sneakers
    while True:
        user_input = input("Continue? Type 'y to continue or 'n' to exit ")

        if user_input == 'n':
            print("exiting the sneaker inventory log")
            exit()

        gather_sneaker_data()

    # Call the function
    sneaker_inventory_log()

