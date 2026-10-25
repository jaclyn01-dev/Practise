"""
slidesScraper.py
KM-03 . KT02 Web scraping  -  built from the slides in your Teams screenshots

What the slides give us (and what this file uses):
    - "Read the page source like a scraper does"   -> the HTML of one book card
    - "Find elements by tag, class and CSS selector" -> the Beautiful Soup cheat sheet
    - "A sitemap lists a site's pages in one file"   -> the <loc> reading code
    - "Pick the tool that matches the page"          -> Requests + Beautiful Soup
    - "Build the Books to Scrape dataset" (Practical 1) -> the to-do list
    - "Every page is a request and a response"       -> the HTTP status codes
    - "Validate content and structure before you trust data" -> validate()
    - "An index finds rows without reading the whole table"  -> the SQLite index

Slides with no code in them (concepts only): module roadmap, classification
software, OCR/ICR/OMR (pytesseract is only named as a demo idea), least
privilege, index types, primary vs secondary data, Activity 1.

Markers used below:
    # SLIDE : copied (or almost copied) from a slide
    # GLUE  : a few lines I added so the pieces run together
    # CODE PACK : taken from your instructor's 02_books_scraper.py
    # TODO  : the slides in these screenshots do not show this part. Yours to write.

Run it:   python slidesScraper.py
Needs:    pip install requests beautifulsoup4
"""

import csv
import sqlite3
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

URL = "https://books.toscrape.com/"      # SLIDE: Books to Scrape (1000 books, 50 pages)
MAX_PAGES = 3                            # GLUE: Practical 1 says 50. Start small.
DB_FILE = "slides_books.db"              # GLUE: file name for the SQLite database

# GLUE: the slide validates "rating between 0 and 5" and "price is a float",
# but the page gives the rating as a word (class="star-rating Three").
RATING_WORDS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


# ----------------------------------------------------------------------------
# Practical 1, step 1: "Check robots.txt ... and record the result."
# ----------------------------------------------------------------------------
def check_robots():
    # GLUE: the slide only shows what a robots.txt looks like (User-agent,
    # Disallow, Allow, Crawl-delay, Sitemap). Here we just download it and
    # print it, so YOU read the rules and record the result.
    resp = requests.get(urljoin(URL, "robots.txt"))
    print("robots.txt status:", resp.status_code)
    print(resp.text)
    # TODO: decide from the rules whether this path is allowed, then stop if not.


# ----------------------------------------------------------------------------
# Steps 1-2 (Request, Response) and 3-4 (Parse, Extract) for ONE page
# ----------------------------------------------------------------------------
def scrape_page(page_url):
    resp = requests.get(page_url)        # SLIDE: "Send HTTP GET to the URL"
    # TODO: the "Your first request" slide is not in these screenshots, so
    # headers (User-Agent) and a timeout are not added here yet.

    # SLIDE: HTTP status: 200 OK, 404 missing, 403 blocked, 429 too many.
    # GLUE: only a 200 is worth parsing, so stop on anything else.
    print("  status:", resp.status_code)
    if resp.status_code != 200:
        print(f"  Not parsing {page_url} (status {resp.status_code})")
        return [], None
    resp.encoding = "utf-8"   # GLUE: stops the pound sign turning into a garbled "Â£"

    soup = BeautifulSoup(resp.text, "html.parser")        # SLIDE: build the tree

    books = []
    for card in soup.select("article.product_pod"):       # SLIDE: 20 per page
        link = card.select_one("h3 a")                     # SLIDE: article h3 a
        price = card.select_one("p.price_color")           # SLIDE: p.price_color
        stars = card.select_one("p.star-rating")           # SLIDE: class="star-rating Three"
        # CODE PACK (02_books_scraper.py): stock is p.availability. No slide
        # shows this selector.
        stock = card.select_one("p.availability")

        books.append({
            # SLIDE tip: the visible title is cut off, the full title is in
            # the title attribute.
            "title": link.get("title", ""),
            "price": price.get_text(strip=True),           # SLIDE: e.g. "£51.77"
            "rating": RATING_WORDS.get(stars["class"][1]),  # SLIDE: ['star-rating', 'Three'] -> 3
            "availability": stock.get_text(strip=True) if stock else "",   # CODE PACK
            # GLUE: the slide's href is relative ("catalogue/a-light.../index.html"),
            # so we join it onto the page address to get a full URL.
            "url": urljoin(page_url, link["href"]),
        })

    # SLIDE: li.next a  = the "next" link  (None on the last page)
    nxt = soup.select_one("li.next a")
    next_url = urljoin(page_url, nxt["href"]) if nxt else None
    return books, next_url


# ----------------------------------------------------------------------------
# Optional: read every <loc> from a sitemap (slide: "A sitemap lists a site's
# pages in one file"). Not used below, because we follow the Next link instead.
# ----------------------------------------------------------------------------
def sitemap_urls(sitemap_url):
    resp = requests.get(sitemap_url)
    soup = BeautifulSoup(resp.content, "xml")             # SLIDE (needs: pip install lxml)
    return [loc.text for loc in soup.find_all("loc")]     # SLIDE


# ----------------------------------------------------------------------------
# Slide: "Validate content and structure before you trust data"
#   Rules for consistency:  data type . range . uniqueness .
#                           consistent expressions . no null values
#   "Garbage in = garbage out"
# ----------------------------------------------------------------------------
def validate(books):
    good, seen_urls = [], set()
    dropped = {"type": 0, "range": 0, "duplicate": 0, "null": 0}

    for b in books:
        # Rule: no null values ("every row has a title")
        title = " ".join((b["title"] or "").split())   # GLUE: tidy spacing too
        if not title or b["rating"] is None:
            dropped["null"] += 1
            continue

        # Rule: data type ("price is a float, not text")
        # GLUE: keep only the digits and the dot, so "£51.77" becomes 51.77
        digits = "".join(ch for ch in b["price"] if ch.isdigit() or ch == ".")
        try:
            price = float(digits)
        except ValueError:
            dropped["type"] += 1
            continue

        # Rule: range ("rating between 0 and 5")
        if not (0 <= b["rating"] <= 5):
            dropped["range"] += 1
            continue

        # Rule: uniqueness ("one row per product URL")
        if b["url"] in seen_urls:
            dropped["duplicate"] += 1
            continue
        seen_urls.add(b["url"])

        # Rule: consistent expressions ("Street", never St. / Str)
        # TODO: nothing in a book listing needs this, but a real dataset
        #       (addresses, categories) would.

        good.append({"title": title, "price": price, "rating": b["rating"],
                     "availability": b["availability"], "url": b["url"]})

    print(f"Validation: kept {len(good)} of {len(books)}. Dropped: {dropped}")
    return good


# ----------------------------------------------------------------------------
# Slide: "An index finds rows without reading the whole table"
# The two SQL statements below are copied from the slide. The Python around
# them (connect, create the table, insert) is GLUE.
# ----------------------------------------------------------------------------
def save_sqlite(books, path=DB_FILE):
    conn = sqlite3.connect(path)
    conn.execute("DROP TABLE IF EXISTS books")      # GLUE: start fresh each run
    conn.execute(
        "CREATE TABLE books ("
        "title TEXT NOT NULL, price REAL, rating INTEGER, "
        "availability TEXT, url TEXT PRIMARY KEY)"
    )
    conn.executemany(
        "INSERT INTO books VALUES (?, ?, ?, ?, ?)",
        [(b["title"], b["price"], b["rating"], b["availability"], b["url"])
         for b in books],
    )

    # SLIDE: -- scraped books table in SQLite
    conn.execute("CREATE INDEX idx_books_title ON books(title)")

    # SLIDE: -- now this uses the index
    # ('Soumission' is on page 1 of the site, so it is in the first 3 pages.)
    row = conn.execute(
        "SELECT price FROM books WHERE title = 'Soumission'"
    ).fetchone()
    print("Index lookup, price of 'Soumission':", row)

    conn.commit()
    conn.close()


# ----------------------------------------------------------------------------
# Practical 1, step 3: run for the pages and save books.csv
# ----------------------------------------------------------------------------
def main():
    check_robots()

    all_books = []
    url, page = URL, 0
    while url and page < MAX_PAGES:                       # GLUE: your while loop
        page += 1
        print(f"Page {page}: {url}")
        books, url = scrape_page(url)
        all_books.extend(books)
        time.sleep(2)     # GLUE: slide caution: scraping can crash a server, be polite

    all_books = validate(all_books)       # Validate before you trust it

    # Step 5, Store: "CSV, JSON or a database". We do the CSV and the database.
    with open("slides_books.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["title", "price", "rating", "availability", "url"])
        writer.writeheader()
        writer.writerows(all_books)
    print(f"Saved {len(all_books)} books to slides_books.csv")

    save_sqlite(all_books)
    print(f"Saved {len(all_books)} books to {DB_FILE}")

    # DONE (Practical 1, step 2): stock is now the "availability" column. The
    #      selector comes from the code pack, not from a slide. Open DevTools
    #      (F12) on a book card and find p.availability yourself to see why.
    # TODO (Practical 1, step 4): open each book's own page and add the UPC and
    #      category.
    # TODO (Practical 1, step 5): how many 5-star books? Average price per
    #      rating? Cheapest book? The data is clean now (price is a float and
    #      rating is a number), so this is a SELECT on the database, or a
    #      loop over all_books.


if __name__ == "__main__":
    main()
