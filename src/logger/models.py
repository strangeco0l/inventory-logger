from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path
import shutil



@dataclass
class Sneaker:
    user_id: str
    purchase_date: str
    retailer: str
    release_date: Optional[str] = None
    size: str = ""
    brand: str = ""
    model: str = ""
    colorway: str = ""
    sku: str = ""
    retail_price: float = 0.0
    resale_price: Optional[float] = None
    quantity: int = 1
    profit_per: float = field(init=False)
    profit: float = field(init=False)

    # New fields for images
    image_path: Optional[str] = None
    thumb_path: Optional[str] = None

    def __post_init__(self):
        # Calculate profits safely
        if self.resale_price is not None:
            self.profit_per = round(self.resale_price - self.retail_price, 2)
            self.profit = round(self.profit_per * self.quantity, 2)
        else:
            self.profit_per = 0.0
            self.profit = 0.0

    def save_uploaded_image(self, source_path):
        """Copies a user-uploaded image into the images/ folder."""
        images_dir = Path("images")
        images_dir.mkdir(exist_ok=True)
        dest = images_dir / Path(source_path).name
        shutil.copy(source_path, dest)
        self.image_path = str(dest)
        return self.image_path

    # def fetch_image(self, throttle: float = 1.0):
    #     """
    #     Fetches a sneaker image from DuckDuckGo using brand+model and SKU.
    #     Stores the paths in image_path and thumb_path.
    #     """
    #     try:
    #         title = f"{self.brand} {self.model}"
    #         img_path, thumb_path = fetch_sneaker_image(title=title, sku=self.sku, throttle=throttle)
    #         self.image_path = img_path
    #         self.thumb_path = thumb_path
    #     except Exception as e:
    #         print(f"Failed to fetch image for {self.brand} {self.model}: {e}")
    #         self.image_path = None
    #         self.thumb_path = None


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

