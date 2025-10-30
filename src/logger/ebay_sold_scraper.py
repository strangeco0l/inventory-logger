import os
import base64
import requests
from dotenv import load_dotenv
from statistics import mean

load_dotenv()

def get_ebay_token():
    """Obtain an OAuth2 token using client credentials."""
    client_id = os.getenv("EBAY_CLIENT_ID")
    client_secret = os.getenv("EBAY_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise ValueError("Missing eBay credentials in .env")

    credentials = f"{client_id}:{client_secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {encoded_credentials}",
    }

    data = {
        "grant_type": "client_credentials",
        "scope": "https://api.ebay.com/oauth/api_scope",
    }

    url = "https://api.ebay.com/identity/v1/oauth2/token"
    response = requests.post(url, headers=headers, data=data)

    if response.status_code != 200:
        raise ValueError(f"Failed to get token: {response.text}")

    return response.json()["access_token"]

def get_average_sold_price(query: str, limit: int = 5) -> float:
    """Fetch sold listings and calculate average sold price."""
    token = get_ebay_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "X-EBAY-C-ENDUSERCTX": "contextualLocation=country=US",
    }

    url = "https://api.ebay.com/buy/browse/v1/item_summary/search"
    params = {
        "q": query,
        "filter": "soldItems:true",
        "limit": str(limit),
        "sort": "-endTime",
    }

    resp = requests.get(url, headers=headers, params=params)
    if resp.status_code != 200:
        raise ValueError(f"Search failed: {resp.status_code} {resp.text}")

    data = resp.json()
    prices = []

    for item in data.get("itemSummaries", []):
        price_info = item.get("price")
        if price_info and "value" in price_info:
            try:
                prices.append(float(price_info["value"]))
            except ValueError:
                continue

    if not prices:
        print("⚠️ No sold prices found.")
        return 0.0

    avg_price = round(mean(prices), 2)
    print(f"✅ Average sold price for '{query}' (last {len(prices)} sales): ${avg_price}")
    return avg_price


if __name__ == "__main__":
    query = "Jordan 1 Retro Chicago Lost and Found"
    print(get_average_sold_price(query))
