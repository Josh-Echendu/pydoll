from pydoll.browser import Chrome
from pydoll.constants import By
from pydoll.commands.input_commands import InputCommands

import random
import asyncio


async def mouse_right_click():
    async with Chrome() as browser:

        tab = await browser.start()

        await tab.go_to("http://omayo.blogspot.com")

        double_click_target = await tab.find_or_wait_element(By.ID, "testdoubleclick", find_all=False, raise_exc=True)

        bounds = await double_click_target.get_bounds_using_js()
        print(bounds)

        x = bounds['x'] + bounds['width']
        y = bounds['y'] + bounds['height']

        double_click_cmd = InputCommands.dispatch_mouse_event(type='mousePressed', pointer_type='mouse', x=x, y=y, button='left', click_count=2)
        await tab._connection_handler.execute_command(double_click_cmd)

        await asyncio.sleep(30)  # Allow time to observe the click effect

        await tab.close()


if __name__ == "__main__":
    asyncio.run(mouse_right_click())








        