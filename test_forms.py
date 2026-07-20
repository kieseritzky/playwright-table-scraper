import asyncio
from playwright.async_api import async_playwright, expect

BASE_URL = "https://qaplayground.com/practice/forms"
async def s01_login_form(context):
    print("[S01] Filling Login Form...")
    page = await context.new_page()
    await page.goto(BASE_URL)
    await page.get_by_label("Email").fill("bot@gmail.com")
    await page.get_by_label("Password").nth(0).fill("alpha")
    await page.get_by_role("button", name="Login").click()
    await expect(page.locator("#loginResult")).to_be_visible()
    print("Success: Logged in successfully")
    await page.wait_for_event("close", timeout=0)

async def s02_pers_det_form(context):
    print("[S02] Filling Personal Detail Form...")
    page = await context.new_page()
    await page.goto(BASE_URL)
    await page.get_by_placeholder("First Name").fill("bot")
    await page.get_by_placeholder("Last Name").fill("test")
    await page.get_by_placeholder("10-digit number").fill("0123456789")
    await page.get_by_test_id("input-dob").fill("2006-12-25")
    await page.get_by_test_id("radio-gender-male").check()
    await page.get_by_test_id("btn-personal-submit").click()
    print("Success: Saved Details Successfully.")
    await page.wait_for_event("close", timeout=0)

async def s03_address_form(context):
    print("[S03] Filling the Address Form...")
    page = await context.new_page()
    await page.goto(BASE_URL)
    await page.get_by_test_id("select-country").select_option(label="Canada")
    await page.get_by_placeholder("Enter city").fill("Otawa")
    await page.get_by_label("About You").fill("I am nobody.")
    await page.get_by_test_id("btn-address-submit").click()
    await expect(page.get_by_test_id("result-address")).to_be_visible()
    print("Success: Address saved successfully.")
    await page.wait_for_event("close", timeout=0)

async def s04_interests_form(context):
    print("[S04] Starting Filling Interests Form...")
    page = await context.new_page()
    await page.goto(BASE_URL)
    await page.get_by_test_id("btn-interests-submit").click()
    await expect(page.get_by_text("select at least")).to_be_visible()
    await page.get_by_test_id("checkbox-interest-playwright").check()
    await page.get_by_test_id("btn-interests-submit").click()
    print("Success: Interests saved successfully!")
    await page.wait_for_event("close", timeout=0)
    
async def s05_acc_setup_form(context):
    print("[S05] Setting Up Account...")   
    page = await context.new_page() 
    await page.goto(BASE_URL)
    await page.get_by_test_id("input-password").fill("123")
    await page.get_by_test_id("input-confirm-password").fill("12")
    await page.get_by_test_id("submit-form-btn").click()
    await expect(page.get_by_test_id("error-confirm-password")).to_be_visible()
    await expect(page.locator("#termsError")).to_be_visible()
    await page.get_by_test_id("input-password").fill("123456")
    await page.get_by_test_id("input-confirm-password").fill("123456")
    await page.get_by_test_id("checkbox-terms").check()
    await page.get_by_test_id("submit-form-btn").click()
    await expect(page.get_by_test_id("form-success-msg")).to_be_visible()
    await expect(page.get_by_test_id("submitted-name")).to_be_visible()
    print("Success: Account setup complete!")
    await page.wait_for_event("close", timeout=0)


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        await asyncio.gather(
             s01_login_form(context),
             s02_pers_det_form(context),
             s03_address_form(context),
             s04_interests_form(context),
             s05_acc_setup_form(context),
        )
if __name__ == "__main__":
    asyncio.run(main())