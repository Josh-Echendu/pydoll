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
        await tab.go_to("https://www.opera.com/download")
        await asyncio.sleep(3)

        pop_up = await tab.find_or_wait_element(By.CLASS_NAME, 'popup')
        await (await pop_up.find_or_wait_element(By.XPATH, "//span[text()='Accept all']")).click()


if __name__ == "__main__":
    asyncio.run(check_button_enabled())
