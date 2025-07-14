from pydoll.browser import Chrome
from pydoll.constants import By
import asyncio

async def webpage_title():
    async with Chrome() as browser:
        tab = await browser.start()
        await tab.go_to('https://www.selenium.dev/')
        await asyncio.sleep(5)

        page_title = await tab.execute_script("document.title")
        page_title = page_title['result']['result']['value']
        print(page_title)

async def main():
    await webpage_title()

asyncio.run(main())
