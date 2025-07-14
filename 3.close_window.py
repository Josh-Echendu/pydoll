import asyncio
from pydoll.browser.chromium import Chrome

async def close_window_example():
    async with Chrome() as browser:
        tab = await browser.start()
        await tab.go_to('https://www.selenium.dev/')
        await asyncio.sleep(2)

        # Close the current tab (window)
        await tab.close()

if __name__ == "__main__":
    asyncio.run(close_window_example())
