import sqlite3
import os
import random
from datetime import datetime, timedelta

# Find our database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "market_delta.db")

def seed_history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Get the ALL products
    cursor.execute("SELECT id, title FROM products")
    products = cursor.fetchall()


    if not products:
        print("No products found! Add a book via the dashboard first.")
        return

    for p_id, title in products:
        print(f"Generating data for: {title}...")

        # Start with a random base price and move it up/down
        base_price = random.uniform(10.0, 60.0)

        fake_data = []
        
        for i in range (5, 0, -1):

            # Create a slight random for the price
            historical_price = round(base_price + random.uniform(-5.0, 5.0), 2)
            timestamp = (datetime.now() - timedelta(days=i)).isoformat()

            fake_data.append((p_id, historical_price, 10, timestamp))

        # 3. Insert the batch for the product
        cursor.executemany('''
            INSERT INTO price_history (product_id, price, stock, timestamp)
            VALUES (?, ?, ?, ?)
        ''', fake_data)

    conn.commit()
    conn.close()
    print("SUCCESS: Global history injection complete")

if __name__ == "__main__":
    seed_history()