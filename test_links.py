import asyncio
from playwright.async_api import async_playwright, expect
import csv


BASE_URL = "https://qaplayground.com/practice/links"
# ------------------------------------------------------------
# INDEPENDENT SCENARIO WORKERS EACH HANDLES ITS OWN STATE
# ------------------------------------------------------------
async def run_s01_internal(context):
    page = await context.new_page()
    await page.goto(BASE_URL)
    print("[S01] Starting Internal Links Test...")
    about_link = page.get_by_test_id("link-internal-about")
    await about_link.click()
    await expect(page).to_have_url("https://qaplayground.com/about-us")
    print("[S01] Success: Internal Link verified.")
    await page.close()

async def run_s02_external(context):
    page = await context.new_page()
    await page.goto(BASE_URL)
    print("[S02] Starting External Link Test...")
    selenium_link = page.get_by_test_id("link-external-selenium")
    await expect(selenium_link).to_have_attribute("target", "_blank")

    async with context.expect_page() as new_page_info:
        await selenium_link.click()
    new_page = await new_page_info.value
    await new_page.wait_for_load_state()
    print("[S02] Success: External link opened in a new tab.")
    await new_page.close()
    await page.close()

async def run_s03_broken(context):
    page = await context.new_page()
    await page.goto(BASE_URL)
    print("[S03] Starting Broken Link Test...")
    broken_link = page.get_by_test_id("link-broken-same")
    href = await broken_link.get_attribute("href")
    if href:
        # Construct absolute URL if path is relative
        target_url = page.url + href if href.startswith('/') else href
        response = await page.request.get(target_url)
        assert response.status in [404, 500], f"Expected error status, got {response.status}"
        print(f"[S03] Success: Broken link returned bad status ({response.status}).")        
    await page.close()

async def run_s04_image(context):
    page = await context.new_page()
    await page.goto(BASE_URL)
    print("[S04] Starting Image Link Test...")
    ext_link_img = page.get_by_test_id("link-image-ironman")
    await expect(ext_link_img).to_have_attribute("target","_blank")

    async with context.expect_page() as new_tab_info:
        await ext_link_img.click()
    new_tab = await new_tab_info.value
    await new_tab.wait_for_load_state()
    print("[S04] Success: Image link opened in a new tab.")
    await new_tab.close()
    await page.close()

async def run_s05_button(context):
    page = await context.new_page()
    await page.goto(BASE_URL)
    print("[S05] Starting Home Button Test...")
    home_button = page.get_by_test_id("link-btn-home")
    await home_button.click()
    await expect(page).to_have_url("https://qaplayground.com/")
    print("[S05] Success: Home button works.")
    await page.close()

async def run_s06_anchor(context):
    page = await context.new_page()
    await page.goto(BASE_URL)
    print("[SO6] Starting Anchor Link Test...")
    await page.get_by_test_id("link-text-anchor").click()
    await expect(page).to_have_url(f"{BASE_URL}#anchor-target")
    print("[S06] Success: Anchor scroll verified.")
    await page.close()

# -----------------------------------------------------------------------------
# MAIN ORCHESTRATOR
# -----------------------------------------------------------------------------

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()

        # Firing off all scenarios at once
        print("Launching all test tabs concurrently...\n")
        await asyncio.gather(
            run_s01_internal(context),
            run_s02_external(context),
            run_s03_broken(context),
            run_s04_image(context),
            run_s05_button(context),
            run_s06_anchor(context)
        )
        
        print("\n All concurrent scenarios executed successfully!")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
