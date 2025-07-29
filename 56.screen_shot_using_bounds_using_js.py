
import asyncio
from pydoll.browser import Chrome
from pydoll.commands.dom_commands import DomCommands
from pydoll.commands.page_commands import PageCommands
from pydoll.constants import By
import os
import aiofiles
import base64


async def main():
    async with Chrome() as browser:
        tab = await browser.start()

        # Go to the page
        await tab.go_to("https://tutorialsninja.com/demo/")

        # Wait for page to fully load
        await asyncio.sleep(5)

        search_cmd = await tab.find_or_wait_element(By.CSS_SELECTOR, '.fa.fa-search')
        bounds = await search_cmd.get_bounds_using_js()
        print(bounds)
        
        x = bounds['x']
        y = bounds['y']
        width = bounds['width']
        height = bounds['height']

        capture_cmd = PageCommands.capture_screenshot(
            clip={
                'x': x,
                'y': y,
                "width": width,
                "height": height,
                "scale": 1
            },
            quality=100
        )
        screenshot_result = await tab._connection_handler.execute_command(capture_cmd)

        # 5. Decode and save screenshot
        image_data = base64.b64decode(screenshot_result['result']['data'])

        Base_dir = r"/Users/joshua.echendu/Documents/pydoll/pydoll/screenshot"
        path = os.path.join(Base_dir, 'page1.png')

        async with aiofiles.open(path, 'wb') as file:
            await file.write(image_data)

        # Close tab
        await tab.close()

if __name__ == "__main__":
    asyncio.run(main())
