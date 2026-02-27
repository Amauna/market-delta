import sys
import asyncio
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright
from utils.cleaners import clean_price, clean_stock
from config import SITE_CONFIGS 
from database import init_db, save_scrape_results

async def scrape_book(url, site_key):
    selectors = SITE_CONFIGS.get(site_key)
    
    if not selectors:
        print(f"Error: No config found for {site_key}")
        return None

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        
        raw_title = await page.inner_text(selectors["name"])
        raw_price = await page.inner_text(selectors["price"])
        raw_stock = await page.inner_text(selectors["stock"])
        
        product_data = {
            "title": raw_title.strip(),
            "price": clean_price(raw_price),
            "stock": clean_stock(raw_stock),
            "currency": selectors["currency"],
            "url": url
        }
        
        await browser.close()
        return product_data
    pass
    
def scrape_book_sync(url, site_key):
    selectors = SITE_CONFIGS.get(site_key)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(url)
            page.wait_for_selector(selectors["price"], timeout=10000)

            raw_title = page.inner_text(selectors["name"])
            raw_price = page.inner_text(selectors["price"])
            raw_stock = page.inner_text(selectors["stock"])

            return{
                "title": raw_title.strip(),
                "price": clean_price(raw_price),
                "stock": clean_stock(raw_stock),
                "currency": selectors["currency"],
                "url": url
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
        finally:
            browser.close()

if __name__ == "__main__":

    # Force Initialize Database if they are missing
    init_db()
    
    # Check if a URL was passed from the command line
    if len(sys.argv) > 1:
        url_to_scrape = sys.argv[1]
        print(f"Scraping command line URL: {url_to_scrape}")
        # We use the SYNC version here because it's simpler for a single-shot process
        from playwright.sync_api import sync_playwright 
        data = scrape_book_sync(url_to_scrape, "books_to_scrape")
        if data and "title" in data:
            save_scrape_results(data)
            print("SUCCESS")
        else:
            print("FAILED")
    else:
        # Default test book if no argument is provided
        url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
        data = asyncio.run(scrape_book(url, "books_to_scrape"))
        if data:
            save_scrape_results(data)