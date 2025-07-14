import asyncio
from pydoll.browser import Chrome
import aiofiles
from pydoll.constants import By
from pydoll.browser.options import ChromiumOptions


async def write_page_source(html: str):
    # aiofiles.open() is like Python's open(), but async, its used to open file. encoding="utf-8" tells Python how to save a string to a file
    async with aiofiles.open('omayo_source.html', mode='w', encoding="utf-8") as file: # async with ensures the file is properly opened/closed.

        # await f.write() writes to the file without blocking the event loop.
        await file.write(html)

async def get_html_source():
    options = ChromiumOptions()
    options.add_argument('--start-maximized')
    options.add_argument("--window-size=1920,1080")

    async with Chrome(options=options) as browser:
        tab = await browser.start()
        await tab.go_to("http://omayo.blogspot.com/")
        await asyncio.sleep(3)

        js_result = await tab.execute_script("document.documentElement.outerHTML")
        html_source = js_result["result"]['result']['value']

        print(html_source)
        await write_page_source(html_source)

        await tab.close()

if __name__ == "__main__":
    asyncio.run(get_html_source())
