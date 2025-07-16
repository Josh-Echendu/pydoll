from pydoll.browser import Chrome
from pydoll.constants import By
from pydoll.browser.options import ChromiumOptions
import asyncio

async def multiple_elements():
    options = ChromiumOptions()
    options.add_argument('--start-maximized')
    options.add_argument("--window-size=1920,1080")

    async with Chrome(options=options) as browser:
        tab = await browser.start()
        await tab.go_to("http://omayo.blogspot.com/")
        await asyncio.sleep(3)
        
        select_options = await tab.find_or_wait_element(By.XPATH, "//select[@id='multiselect1']/option", raise_exc=True, find_all=True)
        print(select_options)
        for element in select_options:
            print(await element.text)

        all_links = await tab.find_or_wait_element(By.TAG_NAME, "a", raise_exc=True, find_all=True)
        
        for i, link in enumerate(all_links):
            print(i, link.get_attribute("href"))
            print(await link.text)
        await tab.close()

asyncio.run(multiple_elements())