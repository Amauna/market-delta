import asyncio
from scraper import scrape_book
from database import get_all_products, save_scrape_results, init_db

async def run_pipeline():

    # Ensure DB is ready
    init_db()

    # Get everything we want to track
    products_to_track = get_all_products()

    if not products_to_track:
        print("No products found in the database. Add some first!")
        return
    print(f"Starting update for {len(products_to_track)} products...")

    for url, site_key in products_to_track:
        print(f"Tracking: {url}")

        #Scrape it
        data = await scrape_book(url, site_key)

        #Save and check for alerts
        if data:
            save_scrape_results(data)

            # 'Sleep' for 2 second so we dont get banned for being too fast
            await asyncio.sleep(2)

        else:
            print(f"Failed to scrape {url}")

    print("Pipeline run complete")

if __name__ == "__main__":
    asyncio.run(run_pipeline())