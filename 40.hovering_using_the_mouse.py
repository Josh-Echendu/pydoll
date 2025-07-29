from pydoll.browser import Chrome
from pydoll.constants import By
from pydoll.commands.input_commands import InputCommands
import random
import asyncio

async def random_hover(tab, bounds):

    # ✅ Add subtle offsets to simulate natural movement
    offset_x = random.randint(-15, 15)
    print("Offset X:", offset_x)

    offset_y = random.randint(-5, 5)
    print("Offset Y:", offset_y)


    x = bounds.get('x') + bounds['width']/2 + offset_x
    y = bounds['y'] + bounds['height']/2 + offset_y
    
    move_cmd = InputCommands.dispatch_mouse_event(type="mouseMoved", x=x, y=y, pointer_type="mouse", button="none")
    await asyncio.sleep(0.5)  # Small delay to simulate human-like interaction
    await tab._connection_handler.execute_command(move_cmd)
    return 

async def hover_menu():
    async with Chrome() as browser:
        tab = await browser.start()
        await tab.go_to("https://tutorialsninja.com/demo/index.php?route=product/product&product_id=47&search=HP")

        # Locate the element to hover over
        hover_target = await tab.find(text="Laptops & Notebooks", tag_name='a')

        bounds = await hover_target.get_bounds_using_js()
        print(bounds)

        await random_hover(tab, bounds)

        await asyncio.sleep(7)

        hover_target2 = await tab.find(text='Desktops', tag_name='a')

        bounds2 = await hover_target2.get_bounds_using_js()
        print(bounds2)

        await random_hover(tab, bounds2)

        await asyncio.sleep(30)  # Allow time to observe the hover effect

        await tab.close()

if __name__ == "__main__":
    asyncio.run(hover_menu())
