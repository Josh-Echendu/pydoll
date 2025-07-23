from pydoll.browser import Chrome
from pydoll.constants import By
from pydoll.commands.input_commands import InputCommands
import random
import asyncio


#| Value      | Meaning                              |
#| ---------- | ------------------------------------ |
#| `"none"`   | No button (for movement only) ✅      |
#| `"left"`   | Simulate left mouse button ✅         |
#| `"middle"` | Simulate middle mouse button (wheel) |
#| `"right"`  | Simulate right-click                 |


async def mouse_event(tab, bounds):

    # ✅ Add subtle offsets to simulate natural movement
    offset_x = random.randint(-15, 15)
    print("Offset X:", offset_x)
    
    offset_y = random.randint(-5, 5)
    print("Offset Y:", offset_y)

    x = bounds['x'] + bounds['width']/2 + offset_x
    y = bounds['y'] + bounds['height']/2 + offset_y
    
    move_cmd = InputCommands.dispatch_mouse_event(type="mouseMoved", x=x, y=y, pointer_type="mouse", button="none")
    await asyncio.sleep(0.5)  # Small delay to simulate human-like interaction
    await tab._connection_handler.execute_command(move_cmd)

    return

async def mouse_left_click():
    async with Chrome() as browser:

        tab = await browser.start()

        await tab.go_to("https://tutorialsninja.com/demo/index.php?route=product/product&product_id=47&search=HP")

        # Locate the element to hover over
        hover_target = await tab.find(text="Laptops & Notebooks", tag_name='a')

        bounds = await hover_target.get_bounds_using_js()
        print(bounds)

        print("Bounds:", bounds)

        await mouse_event(tab, bounds)

        selenium_143 = await tab.find(text="Show AllLaptops & Notebooks", tag_name='a')

        bounds2 = await selenium_143.get_bounds_using_js()
        print("Bounds2:", bounds2)

        await mouse_event(tab, bounds2)
        await asyncio.sleep(7)

        x = bounds2["x"] + bounds2["width"] / 2
        y = bounds2["y"] + bounds2["height"] / 2

        # Simulate left mouse click
        down_cmd = InputCommands.dispatch_mouse_event(type="mousePressed", x=x, y=y, pointer_type='mouse', button='left', click_count=1)
        await tab._connection_handler.execute_command(down_cmd)

        up_cmd = InputCommands.dispatch_mouse_event(type="mouseReleased", x=x, y=y, pointer_type='mouse', button='left', click_count=1)
        await tab._connection_handler.execute_command(up_cmd)

        await asyncio.sleep(30)  # Allow time to observe the click effect

        await tab.close()


if __name__ == "__main__":
    asyncio.run(mouse_left_click())





        



