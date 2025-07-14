import asyncio
from pydoll.browser import Chrome
from pydoll.constants import By
from pydoll.browser.options import ChromiumOptions

async def page_display_status():
    options = ChromiumOptions()
    # options.add_argument('--headless=new')
    options.add_argument('--start-maximized')
    options.add_argument("--window-size=1920,1080")

    async with Chrome(options=options) as browser:
        tab = await browser.start()
        await tab.go_to("https://tutorialsninja.com/demo/")

        tal = await tab.find(text="Qafox.com", tag_name='a')

        if await tal._is_element_visible():
            print("element displayed")
            print(await tal.text)

        else:
            print("element not displayes")
        
        await asyncio.sleep(10)

        await tab.close()

if __name__ == "__main__":
    asyncio.run(page_display_status())