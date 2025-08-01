#| Tool     | Syntax                 |
#| -------- | ---------------------- |
#| Selenium | `arguments[0].tagName` |
#| Pydoll   | `argument.tagName`     |



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

        text_area = await tab.find_or_wait_element(By.XPATH, "(//div[@class='widget-content']/textarea)[1]")
        print(text_area.tag_name)

        tag_name = await tab.execute_script("""
            const area = argument;
            return area.tagName;""", text_area)
        print(tag_name)
        print(tag_name["result"]["result"]['value'])


if __name__ == "__main__":
    asyncio.run(check_button_enabled())