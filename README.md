# 🕷️ Web Scraper Project

A Python automation pipeline that scrapes live data from the web, stores it in a local SQLite database, and generates timestamped reports in CSV, Excel, and chart formats — all with a single command.

---

## 📋 Table of Contents

- [Features](#-features)
- [Project Structure](#-project-structure)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Usage](#-usage)
- [How It Works](#-how-it-works)
- [Customizing Data Sources](#-customizing-data-sources)
- [Output Files](#-output-files)
- [Troubleshooting](#-troubleshooting)

---

## ✨ Features

- 📈 **Cryptocurrency prices** — top 10 coins by market cap with 24h change
- 🌤️ **Weather data** — temperature, humidity, wind speed, and conditions per city
- 📰 **News headlines** — titles, summaries, and sources from RSS feeds
- 🛒 **Product listings** — names, prices, and categories from an e-commerce API
- 💾 **SQLite storage** — all data persisted locally, no external database needed
- 📄 **CSV exports** — one file per category, timestamped
- 📊 **Excel workbook** — four sheets in a single `.xlsx` file, timestamped
- 🖼️ **Charts** — five auto-generated `.png` visualizations, timestamped

---

## 📁 Project Structure

```
web-scraper-project/
│
├── scrapers/                   # One scraper module per data source
│   ├── __init__.py
│   ├── quotes.py               # Cryptocurrency data (CoinGecko API)
│   ├── weather.py              # Weather data (Open-Meteo API)
│   ├── news.py                 # News headlines (RSS feeds)
│   └── products.py             # Product listings (Fake Store API)
│
├── database/                   # Database layer
│   ├── __init__.py
│   └── db_manager.py           # Table creation, insert and query functions
│
├── reports/                    # Report generation layer
│   ├── __init__.py
│   └── report_generator.py     # CSV, Excel, and chart generators
│
├── output/                     # Auto-generated, ignored by git
│   ├── csv/                    # Timestamped CSV files
│   ├── excel/                  # Timestamped Excel workbooks
│   └── charts/                 # Timestamped PNG charts
│
├── data/                       # Auto-generated, ignored by git
│   └── scraper_data.db         # SQLite database file
│
├── main.py                     # Entry point — orchestrates the full pipeline
├── requirements.txt            # Python dependencies
├── .gitignore
└── README.md
```

---

## 🛠️ Requirements

- Python 3.8 or higher
- pip
- Internet connection (for scraping)

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/web-scraper-project.git
cd web-scraper-project
```

### 2. Create and activate a virtual environment

```bash
# Create the virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Mac/Linux
source venv/bin/activate
```

> You should see `(venv)` at the start of your terminal prompt.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify the installation

```bash
python main.py --status
```

If everything is set up correctly, you will see:

```
████████████████████████████████████████████████████
  WEB SCRAPER PROJECT
  Started: 2025-03-25 14:00:00
████████████████████████████████████████████████████

✅ Tables created/verified successfully.

════════════════════════════════════════════════════
  DATABASE STATUS
════════════════════════════════════════════════════

📊 Records in database:
   products     → 0 records
   news         → 0 records
   quotes       → 0 records
   weather      → 0 records
```

---

## 🖥️ Usage

> ⚠️ Always run commands from the **project root directory** (`web-scraper-project/`).

### Run the full pipeline

Scrapes all data sources and generates all reports in one command:

```bash
python main.py
```

### Scrape only

Fetches data from all sources and saves it to the database. Does not generate reports:

```bash
python main.py --scrape
```

### Generate reports only

Reads existing data from the database and generates CSV, Excel, and chart files. Useful when you want to re-generate reports without scraping again:

```bash
python main.py --reports
```

### Check database status

Displays the current number of records stored per table:

```bash
python main.py --status
```

### Show help

Lists all available commands:

```bash
python main.py --help
```

---

### Testing individual modules

You can also run each module independently using the `-m` flag:

```bash
# Run a single scraper
python -m scrapers.quotes
python -m scrapers.weather
python -m scrapers.news
python -m scrapers.products

# Check the database
python -m database.db_manager

# Generate reports from existing data
python -m reports.report_generator
```

> ⚠️ Never run scraper files directly with `python scrapers/quotes.py` — this breaks the import paths. Always use `python -m scrapers.quotes` from the root.

---

## ⚙️ How It Works

### Pipeline overview

```
main.py
  │
  ├── 1. create_tables()        Creates SQLite tables if they don't exist
  │
  ├── 2. SCRAPING
  │     ├── scrape_quotes()     Fetches crypto data   → inserts into quotes table
  │     ├── scrape_weather()    Fetches weather data  → inserts into weather table
  │     ├── scrape_news()       Fetches news articles → inserts into news table
  │     └── scrape_products()   Fetches products      → inserts into products table
  │
  ├── 3. count_records()        Prints record counts per table
  │
  └── 4. REPORTS
        ├── generate_csv_reports()    → output/csv/*.csv
        ├── generate_excel_report()   → output/excel/*.xlsx
        └── generate_charts()         → output/charts/*.png
```

### Data sources

| Module | Source | Type | API Key |
|---|---|---|---|
| `quotes.py` | [CoinGecko API](https://www.coingecko.com/en/api) | REST API | ❌ Not required |
| `weather.py` | [Open-Meteo API](https://open-meteo.com/) | REST API | ❌ Not required |
| `news.py` | RSS Feeds | XML/RSS | ❌ Not required |
| `products.py` | [Fake Store API](https://fakestoreapi.com/) | REST API | ❌ Not required |

### Database tables

| Table | Key columns |
|---|---|
| `products` | `name`, `price`, `currency`, `category`, `url`, `scraped_at` |
| `news` | `title`, `source`, `category`, `url`, `summary`, `scraped_at` |
| `quotes` | `symbol`, `name`, `price`, `currency`, `change_24h`, `type`, `scraped_at` |
| `weather` | `city`, `country`, `temperature`, `feels_like`, `humidity`, `description`, `wind_kmh`, `scraped_at` |

Every record includes a `scraped_at` timestamp (ISO 8601 format) set automatically at insertion time. Every report file also includes a `report_generated_at` column with the exact moment the report was created.

---

## 🔧 Customizing Data Sources

### Change the cities for weather data

Open `scrapers/weather.py` and edit the `CITIES` list:

```python
CITIES = ["Bucaramanga", "Bogota", "Medellin", "Cali", "Cartagena"]
```

Replace with any city names you want:

```python
CITIES = ["New York", "London", "Tokyo", "Sydney", "Berlin"]
```

---

### Change the number of cryptocurrencies fetched

Open `scrapers/quotes.py` and edit the `PARAMS` dictionary:

```python
PARAMS = {
    "vs_currency": "usd",   # Change to "eur", "cop", "gbp", etc.
    "per_page": 10,         # Change to any number up to 250
    ...
}
```

---

### Change the news RSS feeds

Open `scrapers/news.py` and edit the `SOURCES` list. Each source needs three fields:

```python
SOURCES = [
    {
        "name": "Reuters - World",                               # Display name
        "url": "https://feeds.reuters.com/reuters/worldNews",   # RSS feed URL
        "category": "world"                                      # Category label
    },
    {
        "name": "NASA News",
        "url": "https://www.nasa.gov/rss/dyn/breaking_news.rss",
        "category": "science"
    }
]
```

Any public RSS feed URL works here. Some reliable options:

| Source | URL |
|---|---|
| Reuters World | `https://feeds.reuters.com/reuters/worldNews` |
| Reuters Tech | `https://feeds.reuters.com/reuters/technologyNews` |
| Al Jazeera | `https://www.aljazeera.com/xml/rss/all.xml` |
| NASA | `https://www.nasa.gov/rss/dyn/breaking_news.rss` |
| NPR News | `https://feeds.npr.org/1001/rss.xml` |
| BBC World | `http://feeds.bbci.co.uk/news/world/rss.xml` |

---

### Replace the product source

Open `scrapers/products.py` and change `API_URL` to point to any REST API that returns a JSON array of products. Each product object should have at minimum a `title`, `price`, and `category` field:

```python
API_URL = "https://fakestoreapi.com/products"  # Replace with your API endpoint
```

If your API uses different field names, update the mapping inside the loop:

```python
for product in products:
    insert_product(
        name=product.get("title"),       # Change "title" to match your API
        price=product.get("price"),      # Change "price" to match your API
        currency="USD",
        category=product.get("category") # Change "category" to match your API
    )
```

---

## 📂 Output Files

All output files are saved inside the `output/` folder, which is excluded from git. Every file name includes a timestamp so exports never overwrite each other.

```
output/
├── csv/
│   ├── products_20250325_142301.csv
│   ├── news_20250325_142301.csv
│   ├── quotes_20250325_142301.csv
│   └── weather_20250325_142301.csv
│
├── excel/
│   └── full_report_20250325_142301.xlsx   ← four sheets: Products, News, Quotes, Weather
│
└── charts/
    ├── crypto_prices_20250325_142302.png
    ├── crypto_change_24h_20250325_142302.png
    ├── weather_temperatures_20250325_142302.png
    ├── products_by_category_20250325_142302.png
    └── news_by_source_20250325_142302.png
```

### Charts generated

| File | Description |
|---|---|
| `crypto_prices` | Bar chart — current price in USD per cryptocurrency |
| `crypto_change_24h` | Horizontal bar chart — 24h price change %, green/red colored |
| `weather_temperatures` | Grouped bar chart — temperature vs feels-like per city |
| `products_by_category` | Pie chart — product distribution by category |
| `news_by_source` | Bar chart — article count per news source |

---

## 🐛 Troubleshooting

### `ModuleNotFoundError: No module named 'database'`

You are running a scraper file directly. Use the `-m` flag from the project root instead:

```bash
# ❌ Wrong
python scrapers/quotes.py

# ✅ Correct
python -m scrapers.quotes
```

### `Failed to resolve host` / `NameResolutionError`

The RSS feed or API URL is unreachable. This usually means the domain no longer exists or is blocking requests. Open the relevant scraper file and replace the URL with a working alternative. See [Customizing Data Sources](#-customizing-data-sources) for working URL options.

### `No data for X, skipping` in reports

The database has no records for that category. Run the scraper first:

```bash
python main.py --scrape
```

### Virtual environment not active

If you see errors about missing packages, make sure the virtual environment is active:

```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `requests` | HTTP requests to APIs and RSS feeds |
| `beautifulsoup4` | Parsing RSS/XML responses |
| `lxml` | XML parser used by BeautifulSoup |
| `pandas` | Data manipulation and CSV/Excel export |
| `openpyxl` | Excel file generation |
| `matplotlib` | Chart generation |

---

*Built with Python 3 — no paid APIs or external databases required.*
