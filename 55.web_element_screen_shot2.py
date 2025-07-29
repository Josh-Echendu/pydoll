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

        Doc_cmd = DomCommands.get_document()
        doc = await tab._connection_handler.execute_command(Doc_cmd)
        root_node_id = doc['result']['root']['nodeId']

        search_cmd = DomCommands.query_selector(selector='.fa.fa-search', node_id=root_node_id)
        search = await tab._connection_handler.execute_command(search_cmd)
        search_node_id = search['result']['nodeId']

        box_cmd = DomCommands.get_box_model(node_id=search_node_id)
        result = await tab._connection_handler.execute_command(box_cmd)
        box = result['result']['model']['content']

        x1, y1, x2, y2, x3, y3, x4, y4 = box

        left = min(x1, x2, x3, x4)
        top = min(y1, y2, y3, y4)

        width = abs(x1 - x2)
        height = abs(y1 - y4)

        capture_cmd = PageCommands.capture_screenshot(
            clip={
                'x': left,
                'y': top,
                "width": width,
                "height": height,
                "scale": 5
            }
        )
        screenshot_result = await tab._connection_handler.execute_command(capture_cmd)

        # 5. Decode and save screenshot
        image_data = base64.b64decode(screenshot_result['result']['data'])

        Base_dir = r"/Users/joshua.echendu/Documents/pydoll/pydoll/screenshot"
        path = os.path.join(Base_dir, 'page.png')

        async with aiofiles.open(path, 'wb') as file:
            await file.write(image_data)

        # Close tab
        await tab.close()

if __name__ == "__main__":
    asyncio.run(main())
