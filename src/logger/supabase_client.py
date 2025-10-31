from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def save_sneaker_api(sneaker):
    data = {
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
