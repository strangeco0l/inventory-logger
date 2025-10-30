from dotenv import load_dotenv
import os

load_dotenv()

EBAY_CLIENT_ID = os.getenv("EBAY_CLIENT_ID")
EBAY_CLIENT_SECRET = os.getenv("EBAY_CLIENT_SECRET")

if not EBAY_CLIENT_ID or not EBAY_CLIENT_SECRET:
    raise ValueError("Missing eBay credentials. Check your .env file.")