from dataclasses import dataclass, field


@dataclass
class Sneaker:
    user_id: str  # <-- Add this line at the top
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
        print("using updated sneaker class with user_id!")
        self.profit_per = self.resale_price - self.retail_price
        self.profit = self.profit_per * self.quantity


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
        self.profit_per = self.resale_price - self.retail_price
        self.profit = self.profit_per * self.quantity


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
        self.profit_per = self.resale_price - self.retail_price
        self.profit = self.profit_per * self.quantity

