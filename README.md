# Playwright Python Table Scraper

An automated data extraction script built with Python and Playwright to programmatically parse and collect structured data from multi-page interactive web tables.

## ⚙️ Core Technical Features
- **Dynamic Pagination**: Evaluates UI element markers to continuously navigate and process multi-page datasets until completion.
- **Fail-Safe Prechecks**: Implements active assertions to intercept empty page states and flag structural issues before execution.
- **Asynchronous Execution**: Utilizes Playwright's Async API framework to optimize runtime efficiency and data retrieval speeds.
- **Structured Data Export**: Sanitizes and structures raw DOM text nodes directly into a portable CSV format.

## 🚀 Setup & Execution Instructions

1. Clone or download this repository to your local system.
2. Install the necessary dependencies and browser binaries:
   ```bash
   pip install -r requirements.txt
   playwright install
   ```
3. Run the automation script:
   ```bash
   python main.py
   ```
