from dataclasses import dataclass, field


@dataclass
class Sneaker:
    user_id: str
    purchase_date: str
    retailer: str
    release_date: str = None
    size: str = ""
    brand: str = ""
    model: str = ""
    colorway: str = ""
    sku: str = ""
    retail_price: float = 0.0
    resale_price: float = None
    quantity: int = 1
    profit_per: float = 0.0
    profit: float = 0.0

    def __post_init__(self):
        if self.resale_price is not None:
            self.profit_per = round(self.resale_price - self.retail_price, 2)
            self.profit = round(self.profit_per * self.quantity, 2)
        else:
            self.profit_per = 0.0
            self.profit = 0.0



    def __post_init__(self):
        self.profit_per = round(self.resale_price - self.retail_price, 2)
        self.profit = round(self.profit_per * self.quantity, 2)


@dataclass
class Collectibles:
    user_id: str  # ✅ This line must exist
    purchase_date: str
    retailer: str
    brand: str
    item: str
    variation: str
    release_date: str = ""
    retail_price: float = 0.0
    resale_price: float = 0.0
    quantity: int = 1
    profit_per: float = 0.0
    profit: float = 0.0

    def __post_init__(self):
        self.profit_per = self.resale_price - self.retail_price
        self.profit = self.profit_per * self.quantity


@dataclass
class Media:
    user_id: str
    purchase_date: str
    retailer: str
    media_type: str
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

