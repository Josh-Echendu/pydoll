import asyncio
from pydoll.browser import Chrome
from pydoll.commands.dom_commands import DomCommands
from pydoll.commands.page_commands import PageCommands
from pydoll.constants import By
import os

async def main():
    async with Chrome() as browser:
        tab = await browser.start()

        # Go to the page
        await tab.go_to("https://tutorialsninja.com/demo/")

        # Wait for page to fully load
        await asyncio.sleep(5)

        search = await tab.find_or_wait_element(By.XPATH, "//span/button[@type='button']", find_all=False, raise_exc=True)
        Base_dir = r"/Users/joshua.echendu/Documents/pydoll/pydoll/screenshot"
        path = os.path.join(Base_dir, 'element1.png')
        await search.take_screenshot(path=path, quality=100)

        # Close tab
        await tab.close()

if __name__ == "__main__":
    asyncio.run(main())
