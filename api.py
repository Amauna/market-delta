import subprocess
import asyncio
import sys
from fastapi.concurrency import run_in_threadpool

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from pydantic import BaseModel
from scraper import scrape_book_sync
from fastapi import FastAPI, HTTPException
from typing import List
from database import get_all_products, get_latest_price
import sqlite3
import os
from fastapi.middleware.cors import CORSMiddleware

class ProductRequest(BaseModel):
    url: str
    site_key: str = "books_to_scrape"


app = FastAPI(title="Market Delta API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, we change this. For now, it allows everything.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/add-product")
async def add_product(request: ProductRequest):
    print(f"Adding new product: {request.url}")
    
    try:
        # RUN IT SYNC
        process = subprocess.Popen(
            [sys.executable, "scraper.py", request.url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # We wait for it to finish (this is a small scrape, so it's fast)
        stdout, stderr = process.communicate()

        if "SUCCESS" in stdout:
            return {"message": "Product added successfully!"}
        else:
            print(f"Scraper Subprocess Error: {stderr}")
            raise HTTPException(status_code=400, detail="Scraper failed to process URL.")
            
    except Exception as e:
        import traceback
        print(f"CRITICAL API ERROR: \n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
# Ensure the API knows where the DB is
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "market_delta.db")

# Get data for the API
def fetch_product_stats():
    """Custom query to get products and their current prices for the dashbaord."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Get the Title, URL, and the most RECENT price from the history table
        query = '''
            SELECT p.id, p.title, p.url, h.price, h.timestamp
            FROM products p
            LEFT JOIN price_history h ON p.id = h.product_id
            WHERE h.id = (
            SELECT id FROM price_history
            WHERE product_id = p.id
            ORDER BY timestamp DESC LIMIT 1
            )
            '''
        
        cursor.execute(query)
        rows = cursor.fetchall()

        results = []
        for row in rows:
            results.append({
            "id": row[0],
            "title": row[1],
            "url": row[2],
            "current_price": row[3],
            "last_updated": row[4]
            })

        return results
    except Exception as e:
        print(f"DATABASE ERROR: {e}")
        return []
    finally:
        conn.close()

@app.get("/")
def root():
    return {"status": "online"}

@app.get("/dashboard-stats")
def get_dashboard():
    return fetch_product_stats()