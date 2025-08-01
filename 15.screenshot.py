import asyncio
from pydoll.browser import Chrome
from pydoll.constants import By
from pydoll.browser.options import ChromiumOptions
import os
import aiofiles
import base64


async def check_button_enabled(BASE_DIR):
    options = ChromiumOptions()
    options.add_argument('--start-maximized')
    options.add_argument("--window-size=1920,1080")

    async with Chrome(options=options) as browser:
        tab = await browser.start()
        await tab.go_to("https://tutorialsninja.com/demo/")
        await asyncio.sleep(3)
        screenshot_path = os.path.join(BASE_DIR, f'tutorial_ninja2.png')
        await tab.take_screenshot(path=screenshot_path)
        print(f"Screenshot saved to: {screenshot_path}")

        # for APIs
        base64_screenshot = await tab.take_screenshot(as_base64=True)

        ## 5. Decode and save screenshot
        image_data = base64.b64decode(base64_screenshot)
        async with aiofiles.open(screenshot_path, 'wb') as file:
            await file.write(image_data)

        await tab.close()
if __name__ == "__main__":
    BASE_DIR = r"/Users/joshua.echendu/Documents/pydoll/pydoll/screenshot"
    asyncio.run(check_button_enabled(BASE_DIR))