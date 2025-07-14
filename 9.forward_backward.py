#| **Action**          | **JavaScript Command** | **PyDoll Equivalent**                           |
#| ------------------- | ---------------------- | ----------------------------------------------- |
#| Go Back (1 Page)    | `history.back()`       | `await tab.execute_script("history.back()")`    |
#| Go Forward (1 Page) | `history.forward()`    | `await tab.execute_script("history.forward()")` |
#| Reload Page         | `history.go(0)`        | `await tab.execute_script("history.go(0)")`     |
#| Go Back N Pages     | `history.go(-N)`       | `await tab.execute_script("history.go(-2)")`    |
#| Go Forward N Pages  | `history.go(N)`        | `await tab.execute_script("history.go(2)")`     |



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

        link = await tab.find(text="onlytestingblog", raise_exc=True, find_all=False)
        await link.click()
        await asyncio.sleep(5)
        await tab.execute_script("history.back()")
        await asyncio.sleep(5)
        await tab.execute_script("history.forward()")
        await asyncio.sleep(5)
        await tab.close()


if __name__ == "__main__":
    asyncio.run(check_button_enabled())


# history.back();       // Goes back one page
# history.forward();    // Goes forward one page
# history.go(-1);       // Same as back()
# history.go(1);        // Same as forward()
# history.go(0);        // Reloads the current page


