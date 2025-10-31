import requests
from config import EBAY_CLIENT_SECRET, EBAY_CLIENT_ID


def search_ebay_sold(query: str, access_token: str, limit=5):
    url = "https://api.ebay.com/buy/browse/v1/item_summary/search"
    params = {
        "q": query,
        "filter": "price:[1..10000],itemEndDate:[2024-01-01T00:00:00.000Z..]",
        "limit": limit,
        "sort": "-itemEndDate"
    }
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get(url, headers=headers, params=params)

    if resp.status_code != 200:
        print("❌ API error:", resp.status_code, resp.text)
        return []

    data = resp.json()
    results = []
    for item in data.get("itemSummaries", []):
        results.append({
            "title": item.get("title"),
            "price": item.get("price", {}).get("value"),
            "currency": item.get("price", {}).get("currency"),
            "condition": item.get("condition"),
            "date_sold": item.get("itemEndDate"),
            "item_web_url": item.get("itemWebUrl"),
        })
    return results


if __name__ == "__main__":
    token = EBAY_CLIENT_SECRET
    items = search_ebay_sold("Jordan 1 Retro High OG Chicago Lost and Found", token, limit=10)
    for i in items:
        print(i)
