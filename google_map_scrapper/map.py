import random
import time
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

user_input = input("Enter the url to be scrapped\n").strip()

MAP_SEARCH_FIELD = "input.UGojuc.fontBodyMedium.EmSKud.lpggsf"
RETRY_ATTEMPTS = 3

CLICK_RESULT = "a.hfpxzc"

NAME_STORE = "h1.DUwDvf.lfPIob"

STORE_DETAIL = "div.Io6YTe.fontBodyMedium.kR99db.fdkmkc"

SOCIAL_MEDIA_HANDLES = "div.u2OlCc"


def human_pause(min_seconds=0.4, max_seconds=1.2):
    time.sleep(random.uniform(min_seconds, max_seconds))


def move_mouse_like_user(page):
    width = random.randint(900, 1400)
    height = random.randint(500, 900)
    page.mouse.move(random.randint(20, 120), random.randint(20, 120), steps=20)
    page.mouse.move(random.randint(200, width), random.randint(120, height), steps=35)
    human_pause(0.1, 0.4)


def goto_with_retry(page, url):
    for attempt in range(1, RETRY_ATTEMPTS + 1):
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            human_pause(1.0, 2.0)
            return
        except PlaywrightTimeoutError:
            if attempt == RETRY_ATTEMPTS:
                raise
            backoff = attempt * random.uniform(1.5, 2.5)
            print(f"Navigation timeout. Retrying in {backoff:.1f}s...")
            time.sleep(backoff)


def type_like_user(locator, text):
    locator.click()
    human_pause(0.2, 0.7)
    locator.type(text, delay=random.randint(60, 140))
    human_pause(0.3, 0.8)


def search_in_maps(page, query):
    goto_with_retry(page, "https://www.google.com/maps")
    move_mouse_like_user(page)

    search_locator = page.locator(MAP_SEARCH_FIELD)
    search_locator.wait_for(state="visible", timeout=20000)

    type_like_user(search_locator, query)
    search_locator.press("Enter")
    human_pause(2.0, 4.0)
    
    # Wait for results to be visible
    page.wait_for_selector(CLICK_RESULT, timeout=20000)

    # Initialize output file
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write("--- MAP SCRAPER RESULTS ---\n\n")

    scraped_count = 0
    scraped_urls = set()
    scroll_attempts = 0

    while scroll_attempts < 5:
        # Get all current results
        result_elements = page.locator(CLICK_RESULT)
        count = result_elements.count()
        new_elements = []
        
        # Collect new indices that haven't been scraped yet
        for i in range(count):
            try:
                href = result_elements.nth(i).get_attribute("href")
                if href and href not in scraped_urls:
                    new_elements.append(i)
            except Exception:
                continue

        if not new_elements:
            # Scroll feed to load more
            print("No new results found. Scrolling...")
            try:
                feed = page.locator('div[role="feed"]')
                if feed.count() > 0:
                    feed.hover()
                    page.mouse.wheel(0, 5000)
                else:
                    if count > 0:
                        result_elements.nth(count - 1).hover()
                        page.mouse.wheel(0, 5000)
            except Exception:
                pass
            human_pause(2.0, 4.0)
            scroll_attempts += 1
            continue
            
        scroll_attempts = 0 # reset since we found new ones

        # Process a batch of up to 10 stores
        batch = new_elements[:10]
        print(f"Processing batch of {len(batch)} stores...")

        for i in batch:
            try:
                elem = page.locator(CLICK_RESULT).nth(i)
                href = elem.get_attribute("href")
                if not href or href in scraped_urls:
                    continue

                elem.scroll_into_view_if_needed()
                human_pause(0.5, 1.0)
                elem.click()
                human_pause(2.0, 4.0)

                # Scrape details
                name = "Not Found"
                detail = ""
                handles = ""

                try:
                    page.wait_for_selector(NAME_STORE, timeout=5000)
                    name_locator = page.locator(NAME_STORE).first
                    name = name_locator.inner_text()
                except PlaywrightTimeoutError:
                    pass
                except Exception:
                    pass

                # Scrape details before scrolling
                try:
                    details_elements = page.locator(STORE_DETAIL).all_inner_texts()
                    detail = " | ".join(details_elements)
                except Exception:
                    pass

                # Now slowly scroll to the bottom to load handles
                try:
                    # Hover over the store name itself to ensure the detail popup is active
                    panel_focus = page.locator(NAME_STORE).first
                    if panel_focus.count() > 0:
                        panel_focus.hover()
                        panel_focus.click() # Focus the pane specifically
                        human_pause(0.5, 1.0)
                    
                    # Scroll slowly 15 times to mimic a human reading/scrolling down
                    for _ in range(15):
                        page.mouse.wheel(0, 400)
                        human_pause(0.2, 0.5)
                        
                except Exception:
                    pass

                try:
                    # Wait generously for the handles to appear after scrolling
                    # Also explicitly wait for the selector to hit the DOM
                    page.wait_for_timeout(3000)
                    try:
                        page.wait_for_selector(SOCIAL_MEDIA_HANDLES, state="attached", timeout=5000)
                    except PlaywrightTimeoutError:
                        # Fallback: maybe they just aren't there
                        pass
                        
                    handles_elements = page.locator(SOCIAL_MEDIA_HANDLES).all_inner_texts()
                    handles = " | ".join(handles_elements)
                except Exception:
                    pass

                # Write to output
                with open("output.txt", "a", encoding="utf-8") as f:
                    f.write(f"Name: {name}\n")
                    f.write(f"Detail: {detail}\n")
                    f.write(f"Handles: {handles}\n")
                    f.write("-" * 40 + "\n")

                scraped_count += 1
                scraped_urls.add(href)
                print(f"Scraped {scraped_count}: {name}")

                # Go back to results list (close detail pane)
                try:
                    back_btn = page.locator('button[aria-label*="Back"], button[aria-label*="search"], button[class*="VfPpkd-icon-LgbsSe"]')
                    if back_btn.count() > 0:
                        back_btn.first.click()
                        human_pause(1.0, 2.0)
                except Exception:
                    pass

            except Exception as e:
                print(f"Error scraping a store: {e}")


def main():
    if not user_input:
        raise ValueError("Input cannot be empty.")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=random.randint(40, 90))
        context = browser.new_context(
            locale="en-US",
            timezone_id="Asia/Kathmandu",
            viewport={"width": 1366, "height": 768},
        )
        page = context.new_page()

        try:
            search_in_maps(page, user_input)
            print("Search performed successfully.")
        finally:
            human_pause(1.0, 2.0)
            context.close()
            browser.close()


if __name__ == "__main__":
    main()
    
