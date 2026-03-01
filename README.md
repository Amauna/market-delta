## Version 1.2:
<img width="1920" height="925" alt="image" src="https://github.com/user-attachments/assets/2599c4d8-cdbf-484f-80c8-a6260e5ddd3c" />


## Version 1.1:
<img width="1869" height="921" alt="image" src="https://github.com/user-attachments/assets/809f3108-847d-4b5b-bc9f-e1ac47ac5f6d" />

# Market Delta v1.1: Enterprise Competitor Intelligence Engine

A high-performance, full-stack data pipeline engineered to monitor e-commerce price fluctuations and stock levels. Market Delta transforms raw web data into actionable business intelligence via an automated "Collect -> Transform -> Store -> Serve" lifecycle.

## 📁 Project Structure
```
market-delta/
├── frontend/             # Enterprise Dashboard (HTML5, Tailwind, Chart.js)
│   └── index.html
├── utils/                # Data Sanitization & Transformation
│   └── cleaners.py
├── api.py                # REST API (FastAPI) & Process Orchestration
├── config.py             # Site-specific Selector Registry
├── database.py           # SQLite Relational Schema & Persistence Logic
├── main.py               # Background Batch Processing Engine
├── run.py                # System Master Launcher
├── scraper.py            # Playwright Scraping Logic (Async/Sync Hybrid)
├── seed_data.py          # Time-Series Data Generator (For Testing)
├── requirements.txt      # Dependency Manifest
└── README.md             # Architecture Documentation
```

## 🚀 The Mission
For emerging e-commerce brands, manual price tracking is a growth bottleneck. Market Delta provides a scalable, automated alternative that tracks historical **"Price Deltas,"** allowing businesses to respond to competitor moves instantly.

## 🛠️ Technical Stack
- **Backend:** Python 3.12, FastAPI (REST API)
- **Automation:** Playwright (Headless Browser Orchestration)
- **Data Engineering:** SQLite (Relational Time-Series Schema)
- **Frontend:** Vanilla JS, Tailwind CSS, Chart.js (High-density Analytics)

## 🧠 Engineering Challenges Solved

### 1. Windows Async/Proactor Loop Conflict
Standard Playwright Async sessions conflict with FastAPI's default Proactor loop on Windows. I resolved this by implementing **Subprocess Isolation**:
- Background updates are launched as independent Python processes, ensuring the API's event loop remains unblocked and stable.

### 2. Relational Time-Series Modeling
Utilized a **Normalized Relational Schema** (`Products` vs. `PriceHistory`) to manage historical data efficiently. This allows for complex SQL-based trend analysis without data redundancy.

### 3. Change Detection & Sanitization
Developed a robust cleaning pipeline to handle messy e-commerce strings, ensuring all data stored is numeric and ready for analytical visualization.

## ✨ Key Features
- **Bulk Ingestion:** Batch track multiple URLs via a single input.
- **Sparkline Analytics:** Real-time price trend visualization.
- **Process Isolation:** High fault tolerance—scraper errors do not affect API uptime.

## ⚡ Quick Start
1. **Environment Setup:**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   playwright install chromium
   ```
2. **Launch System:**
   ```bash
   python run.py
   ```
3. **Seed Visuals:**
   ```bash
   python seed_data.py
   ```

## 📊 V1.1 Roadmap
- [ ] **Cloud Migration:** AWS deployment for 24/7 monitoring.
- [ ] **Webhook Alerts:** Discord/Slack notifications for price drops.
- [ ] **Proxy Integration:** Bypassing anti-bot measures on enterprise retail sites.

