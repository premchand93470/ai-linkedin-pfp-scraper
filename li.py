import csv
import time
import random
from playwright.sync_api import sync_playwright, TimeoutError
from tqdm import tqdm

def ensure_logged_in(page):
    if "feed" in page.url or "login" in page.url:
        print("🔒 Please make sure you're logged in. Re-opening login page...")
        page.goto("https://www.linkedin.com/login")
        input("✅ After logging in again, press Enter to continue...")

def is_valid_profile_picture_url(url):
    if not url:
        return False
    if "media.licdn.com" not in url:
        return False
    if "profile-displayphoto-shrink" not in url:
        return False
    if any(x in url for x in ["ghost_person", "default", "blank", "_100_100", "_200_200"]):
        return False
    return True

def get_profile_picture_url(page, retries=3, wait_time=2):
    selectors = [
        "img.pv-top-card-profile-picture__image",
        "img.pv-top-card-profile-picture",
        "img.profile-photo-edit__preview",
        "img.ivm-view-attr__img--centered"
    ]

    for attempt in range(retries):
        for selector in selectors:
            img = page.query_selector(selector)
            if img:
                src = img.get_attribute("src")
                if is_valid_profile_picture_url(src):
                    return src
        
        images = page.query_selector_all("img")
        for img in images:
            src = img.get_attribute("src")
            if is_valid_profile_picture_url(src):
                return src

        time.sleep(wait_time + random.uniform(0.5, 1.5))  # Wait before retrying
        page.reload()
    
    return "nopfp"

def random_human_pause(min_sec=1.5, max_sec=4.0):
    time.sleep(random.uniform(min_sec, max_sec))

def scroll_page_randomly(page):
    try:
        page.mouse.wheel(0, random.randint(100, 500))
        time.sleep(random.uniform(0.5, 1.5))
    except Exception:
        pass  # scrolling is optional

def take_long_break():
    wait_time = random.randint(300, 600)  # 5 to 10 minutes
    minutes = wait_time // 60
    seconds = wait_time % 60
    print(f"🛌 Taking a break for {minutes} minutes and {seconds} seconds to stay safe...")
    for remaining in range(wait_time, 0, -1):
        mins, secs = divmod(remaining, 60)
        timeformat = f"{mins:02d}:{secs:02d}"
        print(f"⏳ Resuming in {timeformat}", end="\r")
        time.sleep(1)

def load_already_scraped(output_file):
    scraped_urls = set()
    try:
        with open(output_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                url = row.get('LinkedIn URL', '').strip()
                if url:
                    scraped_urls.add(url)
    except FileNotFoundError:
        pass  # No output file yet
    return scraped_urls

def scrape_profile_pictures(input_file, output_file):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://www.linkedin.com/login")
        input("📥 Please log in to LinkedIn manually, then press Enter to continue...")

        scraped_urls = load_already_scraped(output_file)
        print(f"🔎 Found {len(scraped_urls)} already scraped profiles. Skipping them...")

        with open(input_file, newline='', encoding='utf-8') as csvfile:
            reader = list(csv.DictReader(csvfile))
            total_profiles = len(reader)
            fieldnames = reader[0].keys()
            extended_fieldnames = list(fieldnames) + ['Profile Picture URL']

            # Make sure header exists
            if not scraped_urls:
                with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
                    writer = csv.DictWriter(outfile, fieldnames=extended_fieldnames)
                    writer.writeheader()

            for idx, row in enumerate(tqdm(reader, desc="Scraping Profiles", ncols=100)):
                url = row.get('LinkedIn URL', '').strip()
                if not url or url in scraped_urls:
                    continue  # Skip already scraped

                try:
                    ensure_logged_in(page)
                    page.goto(url, timeout=25000)
                    page.wait_for_timeout(random.randint(4000, 6000))  # wait for page load

                    scroll_page_randomly(page)

                    pfp_url = get_profile_picture_url(page, retries=3, wait_time=3)
                    row['Profile Picture URL'] = pfp_url
                    tqdm.write(f"✅ [{idx+1}/{total_profiles}] {url} → {pfp_url}")

                except TimeoutError:
                    tqdm.write(f"⚠️ [{idx+1}/{total_profiles}] Timeout visiting {url}. Skipping...")
                    row['Profile Picture URL'] = "nopfp"
                except Exception as e:
                    tqdm.write(f"⚠️ [{idx+1}/{total_profiles}] Error visiting {url}: {e}")
                    row['Profile Picture URL'] = "nopfp"

                with open(output_file, 'a', newline='', encoding='utf-8') as outfile:
                    writer = csv.DictWriter(outfile, fieldnames=extended_fieldnames)
                    writer.writerow(row)

                random_human_pause(2.5, 6.5)

                if (idx + 1) % 500 == 0 and idx != 0:
                    take_long_break()

        browser.close()
        print("🎯 Scraping completed and saved progressively!")

if __name__ == "__main__":
    scrape_profile_pictures("version1-2kdoc.csv", "output1.csv")
