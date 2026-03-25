import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'scraper_data.db')


def get_connection():
    """Return a connection to the SQLite database."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn


def create_tables():
    """Create all tables if they do not exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # Table: Products
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            name       TEXT NOT NULL,
            price      REAL,
            currency   TEXT DEFAULT 'USD',
            category   TEXT,
            url        TEXT,
            scraped_at TEXT NOT NULL
        )
    ''')

    # Table: News
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            title      TEXT NOT NULL,
            source     TEXT,
            category   TEXT,
            url        TEXT,
            summary    TEXT,
            scraped_at TEXT NOT NULL
        )
    ''')

    # Table: Quotes (crypto / stocks)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quotes (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol     TEXT NOT NULL,
            name       TEXT,
            price      REAL,
            currency   TEXT DEFAULT 'USD',
            change_24h REAL,
            type       TEXT,           -- 'crypto' or 'stock'
            scraped_at TEXT NOT NULL
        )
    ''')

    # Table: Weather
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            city        TEXT NOT NULL,
            country     TEXT,
            temperature REAL,
            feels_like  REAL,
            humidity    INTEGER,
            description TEXT,
            wind_kmh    REAL,
            scraped_at  TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Tables created/verified successfully.")


# ─────────────────────────────────────────────
#  INSERT
# ─────────────────────────────────────────────

def insert_product(name, price, currency='USD', category=None, url=None):
    """Insert a single product record into the database."""
    conn = get_connection()
    conn.execute('''
        INSERT INTO products (name, price, currency, category, url, scraped_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, price, currency, category, url, datetime.now().isoformat()))
    conn.commit()
    conn.close()


def insert_news(title, source=None, category=None, url=None, summary=None):
    """Insert a single news article record into the database."""
    conn = get_connection()
    conn.execute('''
        INSERT INTO news (title, source, category, url, summary, scraped_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (title, source, category, url, summary, datetime.now().isoformat()))
    conn.commit()
    conn.close()


def insert_quote(symbol, name=None, price=None, currency='USD',
                 change_24h=None, type='crypto'):
    """Insert a single quote record into the database."""
    conn = get_connection()
    conn.execute('''
        INSERT INTO quotes (symbol, name, price, currency, change_24h, type, scraped_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (symbol, name, price, currency, change_24h, type, datetime.now().isoformat()))
    conn.commit()
    conn.close()


def insert_weather(city, country=None, temperature=None, feels_like=None,
                   humidity=None, description=None, wind_kmh=None):
    """Insert a single weather record into the database."""
    conn = get_connection()
    conn.execute('''
        INSERT INTO weather (city, country, temperature, feels_like, humidity,
                             description, wind_kmh, scraped_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (city, country, temperature, feels_like, humidity, description,
          wind_kmh, datetime.now().isoformat()))
    conn.commit()
    conn.close()


# ─────────────────────────────────────────────
#  QUERY
# ─────────────────────────────────────────────

def get_products():
    """Return all product records ordered by scrape date descending."""
    conn = get_connection()
    rows = conn.execute('SELECT * FROM products ORDER BY scraped_at DESC').fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_news():
    """Return all news records ordered by scrape date descending."""
    conn = get_connection()
    rows = conn.execute('SELECT * FROM news ORDER BY scraped_at DESC').fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_quotes():
    """Return all quote records ordered by scrape date descending."""
    conn = get_connection()
    rows = conn.execute('SELECT * FROM quotes ORDER BY scraped_at DESC').fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_weather():
    """Return all weather records ordered by scrape date descending."""
    conn = get_connection()
    rows = conn.execute('SELECT * FROM weather ORDER BY scraped_at DESC').fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ─────────────────────────────────────────────
#  UTILITIES
# ─────────────────────────────────────────────

def count_records():
    """Print record counts for each table."""
    conn = get_connection()
    tables = ['products', 'news', 'quotes', 'weather']
    print("\n📊 Records in database:")
    for table in tables:
        count = conn.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]
        print(f"   {table:<12} → {count} records")
    conn.close()


if __name__ == '__main__':
    create_tables()
    count_records()