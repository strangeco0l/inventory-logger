from dataclasses import dataclass, field

@dataclass
class Collectibles:
    purchase_date: str
    retailer: str
    brand: str
    item: str
    variation: str
    retail_price: float
    resale_price: float
    quantity: int = 1
    profit_per: float = field(init=False)
    profit: float = field(init=False)

    def __post_init__(self):
        # Calculate profit after the object is initialized
        self.profit_per = self.resale_price - self.retail_price
        self.profit = self.profit_per * self.quantity


def collectibles_inventory_log():

    def gather_collectibles_data():
        purchase_date = input("Purchase date?: ")
        retailer = input("Retailer?: ")
        brand = input("Brand?: ")
        item = input("Item?: ")
        variation = input("Variation?: ")
        quantity = int(input("Quantity?: "))
        retail = int(input("What did you pay?: "))
        resale = int(input("Whats it worth?: "))

        collectibles = Collectibles(
            purchase_date=purchase_date,
            retailer=retailer.title(),
            brand=brand.title(),
            item=item.title(),
            variation=variation,
            retail_price=retail,
            resale_price=resale,
            quantity=quantity
        )

        from data_handling import save_collectibles_data
        save_collectibles_data(collectibles)

        print("Collectibles logged succesfully!\n")
    gather_collectibles_data()

    while True:
        user_input = input("Continue? Type 'y to continue or 'n' to exit ")

        if user_input == 'n':
            print("exiting the collectibles inventory log")
            exit()

        gather_collectibles_data()

    # Call the function
    collectibles_inventory_log()

