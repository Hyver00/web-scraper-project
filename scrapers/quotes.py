import requests
from database.db_manager import insert_quote

# CoinGecko public API — no API key required
URL = "https://api.coingecko.com/api/v3/coins/markets"

PARAMS = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 10,
    "page": 1,
    "sparkline": False,
    "price_change_percentage": "24h"
}


def scrape_quotes():
    """Fetch top 10 cryptocurrencies by market cap and store them in the database."""
    print("🔄 Fetching cryptocurrency data...")
    try:
        response = requests.get(URL, params=PARAMS, timeout=10)
        response.raise_for_status()
        coins = response.json()

        for coin in coins:
            insert_quote(
                symbol=coin.get("symbol", "").upper(),
                name=coin.get("name"),
                price=coin.get("current_price"),
                currency="USD",
                change_24h=coin.get("price_change_percentage_24h"),
                type="crypto"
            )

        print(f"✅ {len(coins)} cryptocurrencies saved.")
    except requests.RequestException as e:
        print(f"❌ Error fetching crypto data: {e}")


if __name__ == "__main__":
    scrape_quotes()