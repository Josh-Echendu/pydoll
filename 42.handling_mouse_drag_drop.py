from pydoll.browser import Chrome
from pydoll.constants import By
from pydoll.commands.input_commands import InputCommands
import asyncio

async def drag_slider_with_mouse_events():
    async with Chrome() as browser:
        tab = await browser.start()
        await tab.go_to("http://omayo.blogspot.com/p/page3.html")
        await asyncio.sleep(2)

        slider = await tab.find_or_wait_element(By.XPATH, "//a[@aria-labelledby='price-min-label']", timeout=10)
        bounds = await slider.get_bounds_using_js()

        start_x = int(bounds["x"] + bounds["width"] / 2)
        start_y = int(bounds["y"] + bounds["height"] / 2)

        print("Slider position:", start_x, start_y)

        # Step 1: Move mouse to slider
        move_cmd = InputCommands.dispatch_mouse_event(
            type="mouseMoved", x=start_x, y=start_y, button="none", pointer_type="mouse"
        )
        await tab._connection_handler.execute_command(move_cmd)
        await asyncio.sleep(0.2)

        # Step 2: Press down mouse (start drag)
        press_cmd = InputCommands.dispatch_mouse_event(
            type="mousePressed", x=start_x, y=start_y, button="left", click_count=1, pointer_type="mouse"
        )
        await tab._connection_handler.execute_command(press_cmd)
        await asyncio.sleep(0.2)

        # Step 3: Move mouse to the right
        target_x = start_x + 60 # note: + 60 is equal to + 100  and + 120 is equeal to +200, that the simple maths  
        move_right_cmd = InputCommands.dispatch_mouse_event(
            type="mouseMoved", x=target_x, y=start_y, button="none", pointer_type="mouse"
        )
        await tab._connection_handler.execute_command(move_right_cmd)
        await asyncio.sleep(0.2)

        # Step 4: Release mouse (drop)
        release_cmd = InputCommands.dispatch_mouse_event(
            type="mouseReleased", x=target_x, y=start_y, button="left", click_count=1, pointer_type="mouse"
        )
        await tab._connection_handler.execute_command(release_cmd)

        print("✅ Slider moved using raw mouse events.")

        await asyncio.sleep(5)
        await tab.close()

if __name__ == "__main__":
    asyncio.run(drag_slider_with_mouse_events())





# from pydoll.browser import Chrome
# from pydoll.constants import By
# from pydoll.commands.input_commands import InputCommands
# import random
# import asyncio

# async def drag_slider_using_dispatch_drag_event():
#     async with Chrome() as browser:

#         tab = await browser.start()

#         await tab.go_to("http://omayo.blogspot.com/p/page3.html")

#         # Locate the element to hover over
#         hover_target = await tab.find_or_wait_element(By.XPATH, "//a[@aria-labelledby='price-min-label']", timeout=10)

#         bounds = await hover_target.get_bounds_using_js()

#         print("Bounds:", bounds)

#         start_x = int(bounds["x"] + bounds["width"] / 2)
#         start_y = int(bounds["y"] + bounds["height"] / 2)

#         # this tells the browser: “Hey, the mouse just started dragging something at this exact pixel.”
#         drag_enter_cmd = InputCommands.dispatch_drag_event(type="dragEnter", x=start_x, y=start_y)
        
#         # Sends the dragEnter event to the browser using PyDoll’s internal CDP command sender.
#         if await tab._connection_handler.execute_command(drag_enter_cmd):
#             print("About to be dragged.")

#         await asyncio.sleep(2)

#         # this means: “The mouse is being dragged over this new point (100 pixels to the right).”
#         drag_over_cmd = InputCommands.dispatch_drag_event(type="dragOver", x=start_x + 100, y=start_y)
        
#         # Sends the dragOver event to the browser.
#         if await tab._connection_handler.execute_command(drag_over_cmd):
#             print("Drag over command executed successfuly.")

#         # this means: “Let go of the mouse now at this position.”
#         drop_cmd = InputCommands.dispatch_drag_event(type="drop", x=start_x + 100, y=start_y)
        
#         # Sends the drop event to the browser to finalize the drag operation.
#         if await tab._connection_handler.execute_command(drop_cmd):
#             print("Drop command executed successfully.")

#         await asyncio.sleep(30)  # Allow time to observe the click effect

#         await tab.close()


# if __name__ == "__main__":
#     asyncio.run(drag_slider_using_dispatch_drag_event())





        



