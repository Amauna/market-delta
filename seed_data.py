import sqlite3
import os
from datetime import datetime, timedelta

# Find our database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "market_delta.db")

def seed_history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Get the first product ID
    cursor.execute("SELECT id, title FROM products LIMIT 1")
    product = cursor.fetchone()

    if not product:
        print("No products found! Add a book via the dashboard first.")
        return

    p_id, title = product
    print(f"Seeding history for: {title} (ID: {p_id})")

    # 2. Create fake historical prices
    # We'll create prices for the last 5 days
    fake_data = [
        (p_id, 15.50, 19, (datetime.now() - timedelta(days=5)).isoformat()),
        (p_id, 25.00, 19, (datetime.now() - timedelta(days=4)).isoformat()),
        (p_id, 10.00, 19, (datetime.now() - timedelta(days=3)).isoformat()),
        (p_id, 45.99, 19, (datetime.now() - timedelta(days=2)).isoformat()),
        (p_id, 22.65, 19, (datetime.now() - timedelta(days=1)).isoformat()),
    ]

    # 3. Insert them
    cursor.executemany('''
        INSERT INTO price_history (product_id, price, stock, timestamp)
        VALUES (?, ?, ?, ?)
    ''', fake_data)

    conn.commit()
    conn.close()
    print("SUCCESS: 5 days of history injected. Check your dashboard!")

if __name__ == "__main__":
    seed_history()