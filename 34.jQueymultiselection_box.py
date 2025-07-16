import asyncio
from pydoll.browser import Chrome
from pydoll.constants import By
from pydoll.browser.options import ChromiumOptions

async def handle_multiselection():
    options = ChromiumOptions()
    options.add_argument('--start-maximized')

    async with Chrome(options=options) as browser:
        tab = await browser.start()
        await tab.go_to("https://www.jqueryscript.net/demo/Drop-Down-Combo-Tree/#google_vignette")
        await asyncio.sleep(3)

        await (await tab.find_or_wait_element(By.ID, "justAnInputBox")).click()

        await (await tab.find_or_wait_element(By.XPATH, "(//span[contains(text(), 'choice 1')])[1]")).click()
        await (await tab.find_or_wait_element(By.XPATH, "(//span[contains(text(), 'choice 3')])[1]")).click()
        await (await tab.find_or_wait_element(By.XPATH, "(//span[contains(text(), 'choice 5')])[1]")).click()
        await (await tab.find_or_wait_element(By.XPATH, "(//button/span)[1]")).click()
        await asyncio.sleep(3)

if __name__ == "__main__":
    asyncio.run(handle_multiselection())
