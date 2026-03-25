import sys
import time
from datetime import datetime

from database.db_manager import create_tables, count_records
from scrapers.quotes import scrape_quotes
from scrapers.weather import scrape_weather
from scrapers.news import scrape_news
from scrapers.products import scrape_products
from reports.report_generator import generate_all_reports

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────

def print_header(title: str):
    """Print a formatted section header."""
    width = 52
    print(f"\n{'═' * width}")
    print(f"  {title}")
    print(f"{'═' * width}")


def run_step(label: str, fn, errors: list):
    """
    Run a single pipeline step.
    Catches exceptions so one failure doesn't abort the whole pipeline.
    """
    print(f"\n▶  {label}...")
    start = time.time()
    try:
        fn()
        elapsed = time.time() - start
        print(f"   ✔  Done in {elapsed:.2f}s")
    except Exception as e:
        elapsed = time.time() - start
        print(f"   ✘  Failed after {elapsed:.2f}s → {e}")
        errors.append((label, str(e)))


# ─────────────────────────────────────────────
#  MODES
# ─────────────────────────────────────────────

def run_scrape(errors: list):
    """Run all four scrapers sequentially."""
    print_header("STEP 1 · SCRAPING")
    run_step("Cryptocurrencies  (CoinGecko)",  scrape_quotes,   errors)
    run_step("Weather           (Open-Meteo)", scrape_weather,  errors)
    run_step("News              (BBC RSS)",    scrape_news,     errors)
    run_step("Products          (Fake Store)", scrape_products, errors)


def run_reports(errors: list):
    """Generate all reports: CSV, Excel, and charts."""
    print_header("STEP 2 · REPORTS")
    run_step("CSV + Excel + Charts", generate_all_reports, errors)


def run_status():
    """Print current record counts per table."""
    print_header("DATABASE STATUS")
    count_records()


# ─────────────────────────────────────────────
#  SUMMARY
# ─────────────────────────────────────────────

def print_summary(errors: list, start_time: float):
    """Print a final execution summary with timestamp."""
    elapsed = time.time() - start_time
    print_header("EXECUTION SUMMARY")
    print(f"  Finished at : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Total time  : {elapsed:.2f}s")

    if errors:
        print(f"\n  ⚠️  {len(errors)} step(s) had errors:")
        for label, msg in errors:
            print(f"     • {label}: {msg}")
    else:
        print("\n  ✅ All steps completed without errors.")
    print()


# ─────────────────────────────────────────────
#  USAGE MENU
# ─────────────────────────────────────────────

USAGE = """
Usage:
  python main.py              # scrape + generate reports (full pipeline)
  python main.py --scrape     # scrape only
  python main.py --reports    # generate reports only
  python main.py --status     # show database record counts
  python main.py --help       # show this message
"""


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────

def main():
    args   = sys.argv[1:]
    errors = []
    start  = time.time()

    # Banner
    print(f"\n{'█' * 52}")
    print(f"  WEB SCRAPER PROJECT")
    print(f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'█' * 52}")

    if "--help" in args:
        print(USAGE)
        return

    # Always ensure tables exist before any operation
    create_tables()

    if "--status" in args:
        run_status()

    elif "--scrape" in args:
        run_scrape(errors)
        run_status()

    elif "--reports" in args:
        run_reports(errors)

    else:
        # Default: full pipeline — scrape then report
        run_scrape(errors)
        run_status()
        run_reports(errors)

    print_summary(errors, start)


if __name__ == "__main__":
    main()