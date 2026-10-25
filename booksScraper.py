"""
booksScraper.py
KM-03 · KT02 Web scraping and accurate data  (maps to IAC0201, IAC0202, IAC0203)

Scrapes the Books to Scrape practice site (books.toscrape.com), which exists
for scraping practice, and saves the result as books.csv.

The five steps of web scraping (slide "Web scraping basics"):
    1 Request   send an HTTP GET to the URL            -> fetch()
    2 Response  receive the raw HTML                    -> fetch()
    3 Parse     build a searchable tree (BeautifulSoup) -> parse_books()
    4 Extract   select the fields you need              -> parse_books()
    5 Store     CSV, JSON or a database                 -> main()

Run it:
    python booksScraper.py              (first 3 pages, 60 books)
    python booksScraper.py --pages 50   (all 1000 books)

Setup (once, inside your venv):
    pip install requests beautifulsoup4 lxml pandas
"""

# ----------------------------------------------------------------------------
# BEAUTIFUL SOUP CHEAT SHEET (from the KM-03 slides)
#
#   soup = BeautifulSoup(html, "html.parser")   build the tree
#   soup.title.text                  page title
#   soup.find("h3")                  first match
#   soup.find_all("article", class_="product_pod")   every match
#   soup.select("article.product_pod")               CSS selector -> list
#   soup.select_one("p.price_color")                 first match, or None
#   tag.get_text(strip=True)         the inner text
#   tag["href"]                      an attribute (KeyError if missing)
#   tag.get("title", "")             a safe attribute (default if missing)
#   tag["class"]                     a LIST of classes, e.g. ['star-rating', 'Three']
#
#   CSS selector patterns
#       h3              a tag
#       .price_color    a class
#       #main           an id
#       article h3 a    a descendant
#       ul > li         a direct child
#       a[title]        has an attribute
#       li.next a       the "next" link
#
#   Walking the tree: .parent, .children, .find_next()
#   Sitemaps (XML):   BeautifulSoup(resp.content, "xml").find_all("loc")
#   Beautiful Soup never runs JavaScript. If the data only appears after
#   JavaScript runs, use Selenium instead.
# ----------------------------------------------------------------------------

import argparse
import random
import time
from datetime import datetime
from urllib import robotparser
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"
BOT_NAME = "KM03-StudentBot/1.0"          # honest User-Agent: say who you are
HEADERS = {"User-Agent": BOT_NAME}
RATING_WORDS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def check_robots(base_url):
    """Read robots.txt first (responsible scraping checklist).

    Returns the Crawl-delay in seconds (0 if the site does not set one).
    Stops the script if scraping is not allowed.
    """
    rp = robotparser.RobotFileParser()
    rp.set_url(urljoin(base_url, "robots.txt"))
    try:
        rp.read()
    except OSError as err:
        # We could not confirm permission, so we do not scrape.
        raise SystemExit(f"Could not read robots.txt ({err}). Not scraping.")

    if not rp.can_fetch(BOT_NAME, base_url):
        raise SystemExit("robots.txt blocks this path. Do not scrape it.")

    delay = rp.crawl_delay(BOT_NAME)          # None if not set
    print(f"robots.txt: allowed. Crawl-delay: {delay}")
    return delay or 0


def fetch(session, url, retries=3):
    """Steps 1-2: download the page and return its HTML text."""
    for attempt in range(1, retries + 1):
        resp = session.get(url, headers=HEADERS, timeout=20)   # never hang forever

        if resp.status_code in (429, 503):    # "slow down" / "busy": back off
            wait = 5 * attempt
            print(f"  Got {resp.status_code}. Waiting {wait}s (try {attempt}/{retries})")
            time.sleep(wait)
            continue

        if resp.status_code != 200:           # 403 / 404 etc: stop, do not parse
            raise RuntimeError(f"{resp.status_code} for {url}")

        resp.encoding = "utf-8"               # fixes the "Â£" problem
        return resp.text

    raise RuntimeError(f"Gave up on {url} after {retries} tries")


def parse_books(html, page_url):
    """Steps 3-4: parse the HTML and turn each product card into a dict.

    Returns (list_of_books, url_of_next_page_or_None).
    """
    soup = BeautifulSoup(html, "html.parser")           # step 3: build the tree
    books = []

    for card in soup.select("article.product_pod"):     # 20 cards per page
        link = card.select_one("h3 a")
        price = card.select_one("p.price_color")
        stars = card.select_one("p.star-rating")
        stock = card.select_one("p.availability")       # "In stock" (Practical 1, step 2)

        # If the layout changed and something is missing, skip the card
        # instead of crashing (the data-decay risk with Approach 1).
        if link is None or price is None or stars is None:
            print("  Warning: skipped a card with an unexpected layout")
            continue

        books.append({
            "title": link.get("title", ""),                          # full title
            "price_raw": price.get_text(strip=True),                 # e.g. "£51.77"
            "rating": RATING_WORDS.get(stars["class"][1]),           # 'Three' -> 3
            # Stock is nice to have, so a missing tag gives "" instead of skipping the card.
            "availability": stock.get_text(strip=True) if stock else "",
            "url": urljoin(page_url, link["href"]),                  # relative -> absolute
        })

    nxt = soup.select_one("li.next a")                  # the "next" link, or None
    next_url = urljoin(page_url, nxt["href"]) if nxt else None
    return books, next_url


def scrape(max_pages=3, crawl_delay=0):
    """Step 5 (repeat): follow "next" politely until done, return a DataFrame."""
    all_books, url, page = [], BASE_URL, 0

    with requests.Session() as session:       # a Session re-uses the connection
        while url and page < max_pages:
            page += 1
            print(f"Page {page}: {url}")
            html = fetch(session, url)
            books, url = parse_books(html, url)
            all_books.extend(books)
            # Random 1-3 s pause protects the server (or the site's Crawl-delay)
            time.sleep(max(random.uniform(1, 3), crawl_delay))

    return pd.DataFrame(all_books)


def clean(df):
    """Wrangling: make the data usable, then validate it."""
    # Regex strips "£" (and anything not a digit or dot) so the price is a number
    df["price_gbp"] = (
        df["price_raw"].str.replace(r"[^\d.]", "", regex=True).astype(float)
    )
    df["scraped_at"] = datetime.now().isoformat(timespec="seconds")

    # Validate: a price should be between 0 and 100 (slide "Data wrangling")
    bad = df[~((df["price_gbp"] > 0) & (df["price_gbp"] < 100))]
    print(f"Validation: {len(bad)} row(s) outside 0 < price < 100")
    return df


def main():
    parser = argparse.ArgumentParser(description="Books to Scrape scraper")
    parser.add_argument("--pages", type=int, default=3, help="pages to scrape (max 50)")
    parser.add_argument("--out", default="books.csv", help="output CSV file")
    args = parser.parse_args()

    crawl_delay = check_robots(BASE_URL)             # permission check comes first
    df = clean(scrape(args.pages, crawl_delay))

    df.to_csv(args.out, index=False)                 # Store
    print(f"Saved {len(df)} books to {args.out}")
    print(df.groupby("rating")["price_gbp"].mean().round(2))   # avg price per rating

    # TODO (Practical 1, step 4): open each book's page and add the UPC and
    # category. That extension is yours to write.


if __name__ == "__main__":
    main()
