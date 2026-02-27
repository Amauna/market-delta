import subprocess
import sys
import os
import time
import webbrowser

def start_system():
    print("--- MARKET DELTA STARTUP SEQUENCE ---")

    # Start the API in the background
    print("[1/2] Starting API Server...")
    api_process = subprocess.Popen(
        [sys.executable, "-m","uvicorn", "api:app", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    time.sleep(2)

    # Open the Dashboard
    print("[2/2] Opening Dashboard...")
    frontend_path = os.path.abspath("frontend/index.html")
    webbrowser.open(f"file://{frontend_path}")

    print("\nSYSTEM ONLNE.")
    print("Keep this window open to keep the API running.")
    print("Press Ctrl+C to shut down.")

    try:
        while True:
            line = api_process.stdout.readline()
            if line:
                print(f"API LOG: {line.strip()}")
    except KeyboardInterrupt:
        print("\nShutting down...")
        api_process.terminate()

if __name__ == "__main__":
    start_system()