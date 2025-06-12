📸 AI LinkedIn Profile Picture Scraper

Extract high-quality profile picture URLs of doctors from LinkedIn using a smart, resilient AI-powered scraper.

🚀 Project Overview

This scraper automates LinkedIn profile visits, validates image authenticity, and extracts real profile picture URLs using Playwright automation. Human-like interactions and randomized pauses ensure stealthy operation.

🤖 Features

✅ Smart login checkpoint for session continuity

🔁 Retry logic with fallbacks and scrolling for robustness

🔍 Accurate PFP URL extraction (excludes ghost or default images)

🧠 AI-style filtering based on content and image patterns

📊 Progress-aware saving using CSV and tqdm

🔐 Safe scraping with breaks to avoid rate limiting

🧰 Tech Stack

Python 🐍

Playwright 🎭

tqdm for progress tracking

CSV I/O for data storage

📁 Input Format

CSV file with:

LinkedIn URL

📤 Output

Appends to a CSV with:

LinkedIn URL, Profile Picture URL

"nopfp" is stored if no valid image is found.

💻 Run Instructions

pip install playwright tqdm
playwright install
python scrape_profile_pictures.py

Ensure you're logged in when prompted.

🧠 AI/ML Relevance

This project simulates intelligent behavior through:

Visual feature validation (image pattern logic)

Human-like scraping and adaptive waiting

These ideas are core to ethical data collection in AI workflows.

📄 License

MIT License
