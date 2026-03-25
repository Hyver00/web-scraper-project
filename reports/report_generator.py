import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from database.db_manager import get_products, get_news, get_quotes, get_weather

# ─────────────────────────────────────────────
#  PATHS
# ─────────────────────────────────────────────

BASE_DIR   = os.path.join(os.path.dirname(__file__), '..', 'output')
CSV_DIR    = os.path.join(BASE_DIR, 'csv')
EXCEL_DIR  = os.path.join(BASE_DIR, 'excel')
CHARTS_DIR = os.path.join(BASE_DIR, 'charts')


def ensure_dirs():
    """Create output directories if they don't exist."""
    for path in [CSV_DIR, EXCEL_DIR, CHARTS_DIR]:
        os.makedirs(path, exist_ok=True)


def file_timestamp() -> str:
    """Return a filesystem-safe timestamp string: YYYYMMDD_HHMMSS."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def human_timestamp() -> str:
    """Return a human-readable timestamp for report headers."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ─────────────────────────────────────────────
#  CSV REPORTS
# ─────────────────────────────────────────────

def export_csv(df: pd.DataFrame, name: str) -> str:
    """
    Save a DataFrame as a CSV file.
    Filename includes a timestamp so every export is unique.
    Returns the final file path.
    """
    filename = f"{name}_{file_timestamp()}.csv"
    filepath = os.path.join(CSV_DIR, filename)
    df.to_csv(filepath, index=False, encoding='utf-8-sig')
    print(f"   📄 CSV saved → {filepath}")
    return filepath


def generate_csv_reports():
    """Generate one CSV file per data category, all stamped with generation time."""
    print("\n📄 Generating CSV reports...")
    ensure_dirs()
    ts = human_timestamp()

    datasets = {
        "products": get_products(),
        "news":     get_news(),
        "quotes":   get_quotes(),
        "weather":  get_weather()
    }

    for name, rows in datasets.items():
        if not rows:
            print(f"   ⚠️  No data for {name}, skipping.")
            continue
        df = pd.DataFrame(rows)
        # Inject report generation timestamp as the first column
        df.insert(0, "report_generated_at", ts)
        export_csv(df, name)

    print("✅ CSV reports done.")


# ─────────────────────────────────────────────
#  EXCEL REPORT  (one workbook, four sheets)
# ─────────────────────────────────────────────

def generate_excel_report():
    """
    Generate a single Excel workbook with four sheets (one per category).
    Each sheet includes a header row showing the generation timestamp.
    """
    print("\n📊 Generating Excel report...")
    ensure_dirs()
    ts       = human_timestamp()
    filename = f"full_report_{file_timestamp()}.xlsx"
    filepath = os.path.join(EXCEL_DIR, filename)

    datasets = {
        "Products": get_products(),
        "News":     get_news(),
        "Quotes":   get_quotes(),
        "Weather":  get_weather()
    }

    with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
        for sheet_name, rows in datasets.items():
            if not rows:
                # Write an empty sheet with a note
                pd.DataFrame({"info": [f"No data available — {ts}"]}).to_excel(
                    writer, sheet_name=sheet_name, index=False
                )
                continue

            df = pd.DataFrame(rows)
            df.insert(0, "report_generated_at", ts)

            # Write data starting at row 3 to leave space for the metadata header
            df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=2)

            ws = writer.sheets[sheet_name]

            # Row 1: report title and generation timestamp
            ws.cell(row=1, column=1, value=f"Report: {sheet_name}")
            ws.cell(row=1, column=2, value=f"Generated at: {ts}")

            # Auto-fit column widths
            for col in ws.columns:
                max_len = max(
                    (len(str(cell.value)) for cell in col if cell.value), default=10
                )
                ws.column_dimensions[col[0].column_letter].width = min(max_len + 4, 60)

    print(f"   📊 Excel saved → {filepath}")
    print("✅ Excel report done.")
    return filepath


# ─────────────────────────────────────────────
#  CHARTS
# ─────────────────────────────────────────────

def save_chart(fig: plt.Figure, name: str) -> str:
    """Save a matplotlib figure as PNG and return its path."""
    filename = f"{name}_{file_timestamp()}.png"
    filepath = os.path.join(CHARTS_DIR, filename)
    fig.savefig(filepath, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"   🖼️  Chart saved → {filepath}")
    return filepath


def chart_crypto_prices():
    """Bar chart: current crypto prices in USD."""
    rows = get_quotes()
    if not rows:
        print("   ⚠️  No crypto data for chart.")
        return

    df = pd.DataFrame(rows)
    # Keep the latest price per symbol
    df = df.sort_values("scraped_at").drop_duplicates("symbol", keep="last")
    df = df.sort_values("price", ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(df["symbol"], df["price"], color='steelblue', edgecolor='white')

    # Value labels on top of each bar
    for bar in bars:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() * 1.01,
            f"${bar.get_height():,.2f}",
            ha='center', va='bottom', fontsize=8
        )

    ax.set_title(f"Crypto Prices (USD)\nGenerated: {human_timestamp()}", fontsize=13)
    ax.set_xlabel("Symbol")
    ax.set_ylabel("Price (USD)")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()
    save_chart(fig, "crypto_prices")


def chart_crypto_change():
    """Horizontal bar chart: 24h price change % per cryptocurrency."""
    rows = get_quotes()
    if not rows:
        return

    df = pd.DataFrame(rows)
    df = df.sort_values("scraped_at").drop_duplicates("symbol", keep="last")
    df = df.dropna(subset=["change_24h"]).sort_values("change_24h")

    colors = ['#e74c3c' if v < 0 else '#2ecc71' for v in df["change_24h"]]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(df["symbol"], df["change_24h"], color=colors, edgecolor='white')
    ax.axvline(0, color='black', linewidth=0.8, linestyle='--')
    ax.set_title(f"24h Price Change (%)\nGenerated: {human_timestamp()}", fontsize=13)
    ax.set_xlabel("Change (%)")
    plt.tight_layout()
    save_chart(fig, "crypto_change_24h")


def chart_weather_temperatures():
    """Grouped bar chart: temperature vs feels-like temperature per city."""
    rows = get_weather()
    if not rows:
        print("   ⚠️  No weather data for chart.")
        return

    df = pd.DataFrame(rows)
    df = df.sort_values("scraped_at").drop_duplicates("city", keep="last")

    x     = range(len(df))
    width = 0.35
    fig, ax = plt.subplots(figsize=(11, 6))

    ax.bar([i - width / 2 for i in x], df["temperature"], width,
           label="Temperature (°C)", color='#e67e22')
    ax.bar([i + width / 2 for i in x], df["feels_like"],  width,
           label="Feels Like (°C)",   color='#3498db')

    ax.set_xticks(list(x))
    ax.set_xticklabels(df["city"], rotation=20, ha='right')
    ax.set_ylabel("°C")
    ax.set_title(f"Temperature by City\nGenerated: {human_timestamp()}", fontsize=13)
    ax.legend()
    plt.tight_layout()
    save_chart(fig, "weather_temperatures")


def chart_products_by_category():
    """Pie chart: product count per category."""
    rows = get_products()
    if not rows:
        print("   ⚠️  No product data for chart.")
        return

    df     = pd.DataFrame(rows)
    counts = df["category"].value_counts()

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(
        counts.values,
        labels=counts.index,
        autopct='%1.1f%%',
        startangle=140,
        colors=plt.cm.Set3.colors
    )
    ax.set_title(f"Products by Category\nGenerated: {human_timestamp()}", fontsize=13)
    plt.tight_layout()
    save_chart(fig, "products_by_category")


def chart_news_by_source():
    """Bar chart: article count per news source."""
    rows = get_news()
    if not rows:
        print("   ⚠️  No news data for chart.")
        return

    df     = pd.DataFrame(rows)
    counts = df["source"].value_counts()

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(counts.index, counts.values, color='#9b59b6', edgecolor='white')
    ax.set_title(f"Articles per Source\nGenerated: {human_timestamp()}", fontsize=13)
    ax.set_xlabel("Source")
    ax.set_ylabel("Articles")
    plt.xticks(rotation=20, ha='right')
    plt.tight_layout()
    save_chart(fig, "news_by_source")


def generate_charts():
    """Run all chart generators."""
    print("\n🖼️  Generating charts...")
    ensure_dirs()
    chart_crypto_prices()
    chart_crypto_change()
    chart_weather_temperatures()
    chart_products_by_category()
    chart_news_by_source()
    print("✅ All charts done.")


# ─────────────────────────────────────────────
#  MASTER FUNCTION
# ─────────────────────────────────────────────

def generate_all_reports():
    """Run all report generators: CSV, Excel, and charts."""
    print(f"\n{'='*50}")
    print(f"  REPORT GENERATION STARTED")
    print(f"  Timestamp: {human_timestamp()}")
    print(f"{'='*50}")
    generate_csv_reports()
    generate_excel_report()
    generate_charts()
    print(f"\n{'='*50}")
    print(f"  ALL REPORTS GENERATED ✅")
    print(f"  Timestamp: {human_timestamp()}")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    generate_all_reports()