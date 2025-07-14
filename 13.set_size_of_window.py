import asyncio
from pydoll.browser import Chrome
from pydoll.constants import By
from pydoll.browser.options import ChromiumOptions


async def get_html_source():
    options = ChromiumOptions()
    options.add_argument("--window-size=300,800")

    async with Chrome(options=options) as browser:
        tab = await browser.start()
        await tab.go_to("http://omayo.blogspot.com/")
        await asyncio.sleep(3)

        await tab.close()

if __name__ == "__main__":
    asyncio.run(get_html_source())
