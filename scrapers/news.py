import requests
from bs4 import BeautifulSoup
from database.db_manager import insert_news

# BBC Mundo RSS feeds — public, no API key required
SOURCES = [
    {
        "name": "Al Jazeera - World",
        "url": "https://www.aljazeera.com/xml/rss/all.xml",
        "category": "world"
    },
    {
        "name": "NASA News",
        "url": "https://www.nasa.gov/rss/dyn/breaking_news.rss",
        "category": "science"
    }
]


def scrape_news():
    """Fetch news headlines from RSS feeds and store them in the database."""
    print("🔄 Fetching news headlines...")
    total = 0

    for source in SOURCES:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            resp = requests.get(source["url"], headers=headers, timeout=10)
            resp.raise_for_status()

            soup  = BeautifulSoup(resp.content, "xml")
            items = soup.find_all("item")

            for item in items[:15]:  # Max 15 headlines per source
                title   = item.find("title")
                link    = item.find("link")
                desc    = item.find("description")

                insert_news(
                    title=title.text.strip() if title else "No title",
                    source=source["name"],
                    category=source["category"],
                    url=link.text.strip() if link else None,
                    summary=desc.text.strip()[:300] if desc else None  # Trim long summaries
                )
                total += 1

        except requests.RequestException as e:
            print(f"❌ Error fetching {source['name']}: {e}")

    print(f"✅ {total} news articles saved.")


if __name__ == "__main__":
    scrape_news()