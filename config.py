# market-delta/config.py

SITE_CONFIGS = {
    "books_to_scrape": {
        "name": "h1",
        "price": ".price_color",
        "stock": ".availability",
        "currency": "GBP"
    },
    "another_store": {
        "name": "#product-title",
        "price": ".discount-price",
        "stock": ".stock-level",
        "currency": "USD"
    }
}