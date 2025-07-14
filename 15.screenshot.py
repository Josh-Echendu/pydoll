import asyncio
from pydoll.browser import Chrome
from pydoll.constants import By
from pydoll.browser.options import ChromiumOptions
import os

async def check_button_enabled(BASE_DIR):
    options = ChromiumOptions()
    options.add_argument('--start-maximized')
    options.add_argument("--window-size=1920,1080")

    async with Chrome(options=options) as browser:
        tab = await browser.start()
        await tab.go_to("https://tutorialsninja.com/demo/")
        await asyncio.sleep(3)
        screenshot_path = os.path.join(BASE_DIR, f'tutorial_ninja.png')
        await tab.take_screenshot(path=screenshot_path)
        print(f"Screenshot saved to: {screenshot_path}")

        # for APIs
        base64_screenshot = await tab.take_screenshot(as_base64=True)
        print(base64_screenshot)

if __name__ == "__main__":
    BASE_DIR = r"C:\Users\Admin\Music\pydoll\screenshot"
    asyncio.run(check_button_enabled(BASE_DIR))