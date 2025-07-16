import asyncio
from pydoll.browser import Chrome
from pydoll.constants import By
from pydoll.browser.options import ChromiumOptions

async def handle_multiselection():
    options = ChromiumOptions()
    options.add_argument('--start-maximized')

    async with Chrome(options=options) as browser:
        tab = await browser.start()
        await tab.go_to("https://getbootstrap.com/docs/5.3/components/dropdowns/#overview")
        await asyncio.sleep(3)

        # Locate the <select> element
        select_element = await tab.find_or_wait_element(By.XPATH, "(//button[contains(text(), 'Dropdown button')])[1]")
        await select_element.click()

        await (await tab.find_or_wait_element(By.XPATH, "((//button[contains(text(), 'Dropdown button')])[1]//following::ul/li/a[text()='Something else here'])[1]")).click()



        await asyncio.sleep(300)

if __name__ == "__main__":
    asyncio.run(handle_multiselection())