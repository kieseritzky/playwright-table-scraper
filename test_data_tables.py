import asyncio
import csv
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # --- 1. SETUP & SAFETY INITIALIZATION ---
        await page.goto("https://qaplayground.com/practice/data-table")

        # Verify empty_state and thresholds before doing any work
        initial_row_count = await page.locator("#dataTable tbody tr").count()
        assert initial_row_count>0, "Scraper Error: The table is completely empty!"
        empty_msg_locator = page.locator("[data-testid='empty-table-msg']")
        await expect(empty_msg_locator).to_be_hidden()

        #Playwright - count rows and columns - only on first page no pagination used
        
        row_count = await page.locator("#dataTable tbody tr").count()
        col_count = await page.locator("#dataTable thead th").count()
        print(f"Rows: {row_count} Columns: {col_count}")

        # Reading a specific cell
        cell_text = await page.locator("#dataTable tr:nth-child(2) td:nth-child(2)").text_content()
        print("Cell:", cell_text.strip() if cell_text else None)

        # Read all headers
        headers = await page.locator("#dataTable thead th").all_text_contents()
        print(headers)

        # Find row by content
        row = page.locator("[data-testid='book-row']").filter(has_text="Andrew Hunt")
        await expect(row).to_be_visible()
        # await row.locator("[data-testid='btn-edit-book']").click()

        # Iterate all rows with handling pagination
        
        pagination_count = await page.locator("[data-testid='pagination']").locator("button").count()
        names = []
        # for i in range(pagination_count):
            
        #     rows = page.locator("[data-testid='data-table'] tbody tr")
        #     count = await rows.count()
            
        #     for j in range(count):
        #         name = await rows.nth(j).locator("td:nth-child(2)").text_content()
        #         names.append(name)
                
        #     next_button = page.locator("[data-testid='pagination']").locator("button").nth(i+1)
        #     if await next_button.is_disabled():
        #         print("Reached end of the table")
        #         break
        #     await next_button.click()
        while True:
            rows = page.locator("[data-testid='data-table'] tbody tr")
            count = await rows.count()

            for j in range(count):
                name = await rows.nth(j).locator("td:nth-child(2)").text_content()
                names.append(name.strip() if name else "")
            
            next_arrow = page.locator("[data-testid='pagination-next']")
            if await next_arrow.is_disabled():
                print("Clean shutdown: Reached end of the dataset")
                break
            await next_arrow.click()
        print(names)

        with open("scraped_books.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Book Title"])
            for book in names:
                writer.writerow([book])

        await page.pause()



if __name__ == "__main__":
    asyncio.run(main())
