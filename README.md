# Market Delta: Competitor Intelligence Engine

A full-stack, automated data pipeline designed to monitor e-commerce price fluctuations and stock levels in real-time. 

## 🚀 The Mission
Manual price tracking is a bottleneck for emerging e-commerce brands. Market Delta automates the "Collect -> Transform -> Store -> Serve" lifecycle, providing a professional-grade dashboard for competitor analysis.

## 🛠️ Technical Stack
- **Backend:** Python, FastAPI (REST API)
- **Automation:** Playwright (Headless Browser Scraping)
- **Database:** SQLite (Relational Time-Series Data)
- **Frontend:** Tailwind CSS, JavaScript (Vanilla)
- **Orchestration:** Custom Python Orchestrator with Threadpooling

## 🧠 Engineering Challenges Solved
### 1. Windows Async Conflict Resolution
Standard Playwright Async sessions often conflict with FastAPI's Proactor loop on Windows. I implemented a **Threadpooled Synchronous Scraper** for real-time additions and a **Subprocess Isolation** strategy for automated background updates to ensure 100% system uptime.

### 2. Data Normalization
Implemented a Decoupled Architecture where scraping logic is separated from data cleaning (`utils/cleaners.py`) and site-specific selectors (`config.py`). This allows the system to scale to new retailers without modifying the core engine.

### 3. Change Detection (The "Delta")
Designed a SQL-based change detection system that calculates price shifts before persisting new records, enabling "Price Drop" and "Price Hike" alerts.

## ⚡ Quick Start
1. Clone the repo.
2. `pip install -r requirements.txt`
3. `playwright install chromium`
4. `python run.py` (Launches API and Dashboard automatically)

## 📊 V1.0 Preview
- [ ] Automated daily tracking via Task Scheduler
- [ ] Dynamic product registration via Dashboard
- [ ] Real-time price delta analysis