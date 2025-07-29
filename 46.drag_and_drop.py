from pydoll.browser import Chrome
from pydoll.constants import By
from pydoll.commands.input_commands import InputCommands
import asyncio

async def drag_and_drop_first_image():
    async with Chrome() as browser:
        tab = await browser.start()

        # ✅ Go directly to iframe content
        await tab.go_to("https://www.globalsqa.com/demoSite/practice/droppable/photo-manager.html")
        await asyncio.sleep(2)

        # ✅ Locate source and target
        source = await tab.find_or_wait_element(By.CSS_SELECTOR, "#gallery li")
        target = await tab.find_or_wait_element(By.CSS_SELECTOR, "#trash")

        box1 = await source.get_bounds_using_js()
        box2 = await target.get_bounds_using_js()

        src_x = box1["x"] + box1["width"] / 2
        src_y = box1["y"] + box1["height"] / 2
        dst_x = box2["x"] + box2["width"] / 2
        dst_y = box2["y"] + box2["height"] / 2

        # ✅ Dispatch drag sequence
        await tab._connection_handler.execute_command(InputCommands.dispatch_mouse_event(
            type="mouseMoved", x=src_x, y=src_y, button="left", click_count=0, pointer_type="mouse"
        ))

        await tab._connection_handler.execute_command(InputCommands.dispatch_mouse_event(
            type="mousePressed", x=src_x, y=src_y, button="left", click_count=1, pointer_type="mouse"
        ))

        await asyncio.sleep(0.3)

        await tab._connection_handler.execute_command(InputCommands.dispatch_mouse_event(
            type="mouseMoved", x=dst_x, y=dst_y, button="left", click_count=0, pointer_type="mouse"
        ))

        await asyncio.sleep(0.3)

        await tab._connection_handler.execute_command(InputCommands.dispatch_mouse_event(
            type="mouseReleased", x=dst_x, y=dst_y, button="left", click_count=1, pointer_type="mouse"
        ))

        await asyncio.sleep(5)
        await tab.close()

if __name__ == "__main__":
    asyncio.run(drag_and_drop_first_image())
