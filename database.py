import sqlite3
import os
from datetime import datetime
from turtle import title

# This finds the EXACT folder where database.py lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "market_delta.db")

def init_db():
    """Create the tables if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            url TEXT UNIQUE,
            site_key TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            price REAL,
            stock INTEGER,
            timestamp DATETIME,
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"DONE: Database initialized at {DB_PATH}")

def save_scrape_results(data):
    """Save the clean data into the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Get/Create Product ID
        cursor.execute('INSERT OR IGNORE INTO products (title, url, site_key) VALUES (?, ?, ?)', 
                       (data['title'], data['url'], "books_to_scrape"))
        cursor.execute('SELECT id FROM products WHERE url = ?', (data['url'],))
        product_id = cursor.fetchone()[0]
        
        # Get the old price BEFORE saving the new one
        old_price = get_latest_price(product_id)
        new_price = data['price']

        # Compare
        if old_price is None:
            print(f"--- First time tracking {data['title']}. (Base price: ${new_price}) ---")

        #Price drop
        elif new_price < old_price: 
            diff = round(old_price - new_price, 2)
            print(f"!!! PRICE DROP ALERT! {data['title']} is £{diff} cheaper!") 

        #Price increase
        elif new_price > old_price: 
            diff = round(new_price - old_price, 2)
            print(f"!!! PRICE INCREASE {data['title']} went up by £{diff}")
            
        # No change
        else: 
            print(f"--- No price change for {data['title']} ---")

        # Save the new record regardless
        cursor.execute('''
                       INSERT INTO price_history (product_id, price, stock, timestamp)
                       VALUES (?, ?, ?, ?)
                       ''', (product_id, new_price, data['stock'], datetime.now()))
        conn.commit()
        print(f"Database Updated Successfully.")

    except Exception as e:
        print(f"DATABASE CRITICAL ERROR: {e}")
    finally:
        conn.close()

def get_latest_price(product_id):
    """ Fetch the most recent price for a specific product. """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    #Sort by timestamp (newest first) and take only the first row
    cursor.execute('''
        SELECT price FROM price_history 
        WHERE product_id = ? 
        ORDER BY timestamp DESC 
        LIMIT 1
    ''', (product_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    # If the database is empty, return None
    return result[0] if result else None

def get_all_products():
    """Fetch all tracked products from the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT url, site_key FROM products')
    products = cursor.fetchall()
    
    conn.close()
    return products



if __name__ == "__main__":
    init_db()