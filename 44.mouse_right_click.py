from pydoll.browser import Chrome
from pydoll.constants import By
from pydoll.commands.input_commands import InputCommands

import random
import asyncio




async def mouse_right_click():
    async with Chrome() as browser:

        tab = await browser.start()

        await tab.go_to("https://tutorialsninja.com/demo/index.php?route=product/product&product_id=47&search=HP")

        # Locate the element to hover over
        hover_target = await tab.find(text="Laptops & Notebooks", tag_name='a')

        bounds = await hover_target.get_bounds_using_js()

        x = bounds['x'] + bounds['width']/2
        y = bounds['y'] + bounds['height']/2

        move_cmd = InputCommands.dispatch_mouse_event(type='mouseMoved', x=x, y=y, button='none', pointer_type='mouse')
        await tab._connection_handler.execute_command(move_cmd)


        hover_target = await tab.find(text="Show AllLaptops & Notebooks", tag_name='a')
        bounds1 = await hover_target.get_bounds_using_js()

        x1 = bounds1['x'] + bounds1['width']/2
        y1 = bounds1['y'] + bounds1['height']/2

        move_cmd2 = InputCommands.dispatch_mouse_event(type='mouseMoved', x=x1, y=y1, button="none", pointer_type='mouse')
        await tab._connection_handler.execute_command(move_cmd2)

        await asyncio.sleep(5)

        down_cmd = InputCommands.dispatch_mouse_event(type='mousePressed', x=x1, y=y1, button='right', pointer_type='mouse', click_count=1)
        await tab._connection_handler.execute_command(down_cmd)

        await asyncio.sleep(5)

        down_cmd = InputCommands.dispatch_mouse_event(type='mouseReleased', x=x1, y=y1, button='right', pointer_type='mouse', click_count=1)
        await tab._connection_handler.execute_command(down_cmd)


        await asyncio.sleep(30)  # Allow time to observe the click effect

        await tab.close()


if __name__ == "__main__":
    asyncio.run(mouse_right_click())








        