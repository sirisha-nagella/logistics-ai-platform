"""One-off screenshot capture for the README (run manually, NOT part of the app).

Prereqs:
  1. Build the index:  ./venv/bin/python -m scripts.load_knowledge_base
  2. Run the app:      ./venv/bin/python -m streamlit run app.py --server.headless true --server.port 8610
  3. Run this script:  ./venv/bin/python scripts/capture_screenshots.py 8610

Captures the two most representative views into docs/images/.
"""

import sys
from playwright.sync_api import sync_playwright

PORT = sys.argv[1] if len(sys.argv) > 1 else "8610"
BASE = f"http://localhost:{PORT}"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 1000})
    page.goto(BASE, wait_until="networkidle")
    page.wait_for_timeout(3000)

    # Overview (default landing page)
    page.get_by_role("link", name="Overview").click()
    page.wait_for_timeout(2500)
    page.screenshot(path="docs/images/overview.png", full_page=True)
    print("captured overview.png")

    # Ask the Data: navigate, ask a question, wait for the answer, capture
    page.get_by_role("link", name="Ask the Data").click()
    page.wait_for_timeout(1500)
    page.get_by_placeholder("e.g. Which country generates the most revenue?").fill(
        "Which country generates the most revenue?"
    )
    page.get_by_role("button", name="Ask").click()
    page.wait_for_selector("text=Sources", timeout=180000)
    page.wait_for_timeout(1000)
    page.screenshot(path="docs/images/ask-the-data.png", full_page=True)
    print("captured ask-the-data.png")

    browser.close()
