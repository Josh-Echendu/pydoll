import asyncio
from pydoll.browser import Chrome
from pydoll.constants import By
from pydoll.browser.options import ChromiumOptions

async def check_button_enabled():
    options = ChromiumOptions()
    options.add_argument('--start-maximized')
    options.add_argument("--window-size=1920,1080")

    async with Chrome(options=options) as browser:
        tab = await browser.start()
        await tab.go_to("https://tutorialsninja.com/demo/index.php?route=product/product&product_id=47&search=HP")
        await asyncio.sleep(3)

        popup = await tab.find_or_wait_element(By.XPATH, "(//img[@src])[1]")
        await popup.click()

        await asyncio.sleep(4)

        await (await tab.find_or_wait_element(By.XPATH, "//button[@title='Close (Esc)']")).click()

        


if __name__ == "__main__":
    asyncio.run(check_button_enabled())
