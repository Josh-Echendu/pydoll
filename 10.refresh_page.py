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
        await tab.go_to("http://omayo.blogspot.com/")
        await asyncio.sleep(3)
        for i in range(5):
            await tab.refresh()
            # await tab.execute_script("history.go(0)")

            await asyncio.sleep(3)

if __name__ == "__main__":
    asyncio.run(check_button_enabled())