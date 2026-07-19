import re
import asyncio
from playwright.async_api import async_playwright, expect

BASE_URL = "https://qaplayground.com/practice/modals"
async def run_so1_simple(page):
    print("[S01] Starting test case 01")
    await page.get_by_test_id("btn-open-simple-modal").click()
    modal = page.get_by_test_id("modal-simple")
    await expect(modal).to_be_visible()
    print("Success: Modal window is visible.")
    await page.wait_for_timeout(1000)
    await page.get_by_test_id("btn-close-simple-modal").click()
    await page.wait_for_timeout(1000)

async def run_s02_card(page):
    card_course = page.get_by_test_id("card-course").filter(has_text="Advanced Locators")
    print("[S02] Starting test run_s02_card")
    await card_course.get_by_text("Details").click()
    await page.wait_for_timeout(1000)
    await page.get_by_test_id("btn-close-course").click()
    await page.wait_for_timeout(1000)
    print("Success: Opened Repeated Modals Card succesfully!")

async def run_s03_dynamic(page):
    print("[S03] Running s03 dynamic id modal")
    await page.get_by_test_id("btn-open-dynamic-modal").click()
    await page.wait_for_timeout(1000)
    await page.get_by_test_id("modal-dynamic").locator("button[id^='confirm-modal']").click()
    await page.wait_for_timeout(1000)
    print("Success: Located and clicked the modal with dynamic changing id button")

async def run_s04_missing(page):
    print("[S04] Starting test run_s04_missing...")
    await page.get_by_test_id("btn-open-challenge-modal").click()
    await page.wait_for_timeout(1000)
    await page.get_by_label("Accept terms").click()
    await page.wait_for_timeout(1000)
    print("Success: Terms accepted.")
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(BASE_URL)
        await run_so1_simple(page)
        await run_s02_card(page)
        await run_s03_dynamic(page)
        await run_s04_missing(page)
if __name__ == "__main__":
    asyncio.run(main())        

