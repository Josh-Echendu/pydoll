from pydoll.browser import Chrome
from pydoll.constants import By
from pydoll.commands.input_commands import InputCommands
import random


import asyncio


async def hover_menu():
    async with Chrome() as browser:
        tab = await browser.start()
        await tab.go_to("https://tutorialsninja.com/demo/index.php?route=product/product&product_id=47&search=HP")

        # Locate the element to hover over
        hover_target = await tab.find(text="MP3 Players", tag_name='a')

        # 📏 Asks the browser for the element’s position and size on the screen (via JavaScript).
        bounds = await hover_target.get_bounds_using_js()
        print(bounds)

        # creating random offsets to simulate a more natural hover effect
        offset_x = random.randint(-15, 15)
        offset_y = random.randint(-5, 5)

        # Adding a slight random offset to simulate natural movement
        x = bounds['x'] + bounds['width']/2 + offset_x # This helps to avoid issues with elements that may not respond well to direct clicks
        y = bounds['y'] + bounds['height']/2 + offset_y # # The offsets are small to ensure the hover is still effective without moving too far from the element

        move_cmd = InputCommands.dispatch_mouse_event(type="mouseMoved", x=x, y=y, pointer_type="mouse", button="none")

        if await tab._connection_handler.execute_command(move_cmd):
            print("✅ Hover simulated.")
            await asyncio.sleep(30)  # Allow time to observe the hover effect

        else:
            print("❌ Hover simulation failed.")

        await asyncio.sleep(30)  # Allow time to observe the hover effect

        await tab.close()

if __name__ == "__main__":
    asyncio.run(hover_menu())
