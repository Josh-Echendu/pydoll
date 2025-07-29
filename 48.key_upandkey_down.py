from pydoll.browser import Chrome
from pydoll.constants import By, Key
from pydoll.commands.page_commands import PageCommands
from pydoll.commands.dom_commands import DomCommands
from pydoll.commands.runtime_commands import RuntimeCommands
import asyncio

async def main():
    async with Chrome() as browser:
        tab = await browser.start()
        await tab.go_to("https://tutorialsninja.com/demo/index.php?route=account/login")
        await asyncio.sleep(3)

        # ✅ Set all aside links to target="_blank" using JS
        set_blank_targets = RuntimeCommands.evaluate(
            expression="""
                Array.from(document.querySelectorAll("aside div a"))
                     .forEach(a => a.setAttribute("target", "_blank"));
            """,
            return_by_value=False,
            await_promise=False,
            user_gesture=True
        )
        await tab._connection_handler.execute_command(set_blank_targets)

        # ✅ Now proceed with Meta+Click to open each link
        list_of_links = await tab.find_or_wait_element(By.XPATH, "//aside//div/a", find_all=True, raise_exc=True)
        list_of_links = list_of_links[1:]  # skip first

        for link in list_of_links:
            try:
                coord_values = await link.bounds
                coord_keys = ['x1', 'y1', 'x2', 'y2', 'x3', 'y3', 'x4', 'y4']
                bounds = dict(zip(coord_keys, coord_values))

                width = abs(bounds['x1'] - bounds['x2'])
                height = abs(bounds['y1'] - bounds['y4'])

                center_x = bounds['x1'] + width / 2
                center_y = bounds['y1'] + height / 2

                # bounds = await link.get_bounds_using_js()

                # center_x = bounds['x'] + bounds['width']/2
                # center_y = bounds['y'] + bounds['height']/2

                mov_cmd = InputCommands.dispatch_mouse_event(type='mouseMoved',x=center_x,y=center_y,pointer_type='mouse',button='none')

                ctrl_down = InputCommands.dispatch_key_event(type='keyDown',code='MetaLeft',windows_virtual_key_code=91,key='Meta')

                pressed_click_cmd = InputCommands.dispatch_mouse_event(type='mousePressed',x=center_x,y=center_y,pointer_type='mouse',button='left',click_count=1)

                release_click_cmd = InputCommands.dispatch_mouse_event(type='mouseReleased',x=center_x,y=center_y,pointer_type='mouse',button='left',click_count=1)

                ctrl_up = InputCommands.dispatch_key_event(type='keyUp',key='Meta',code="MetaLeft",windows_virtual_key_code=91)

                await tab._connection_handler.execute_command(mov_cmd)
                await tab._connection_handler.execute_command(ctrl_down)
                await tab._connection_handler.execute_command(pressed_click_cmd)
                await tab._connection_handler.execute_command(release_click_cmd)
                await tab._connection_handler.execute_command(ctrl_up)

            except KeyError:
                print("Skipping element with no box model...")
                continue

        await asyncio.sleep(5)

asyncio.run(main())



from pydoll.browser import Chrome
from pydoll.constants import By
from pydoll.exceptions import ElementNotFound
import asyncio
from pydoll.commands.page_commands import PageCommands
from pydoll.connection.connection_handler import ConnectionHandler

from pydoll.commands.dom_commands import DomCommands


async def find_target_frame(tree):
    if tree['frame'].get("name") == 'iframeResult':
        print('Result: ', tree['frame'])
        return tree['frame']
    for child in tree.get('childFrames', []):
        result = await find_target_frame(child)
        if result:
            return result
    return None

async def checkbox_radio_button():
    async with Chrome() as browser:
        tab = await browser.start()

        await tab.go_to("https://www.w3schools.com/html/tryit.asp?filename=tryhtml5_draganddrop")

        frame_tree_cmd = PageCommands.get_frame_tree()
        frame_tree = await tab._connection_handler.execute_command(frame_tree_cmd)
        print(frame_tree)
        print()
        frame_url = frame_tree['result']['frameTree']['childFrames'][0]['frame']['url']

        target_frame = await find_target_frame(frame_tree['result']['frameTree'])
        if not target_frame:
            raise Exception("iframeResult not found")

        frame_id = target_frame["id"]  # ✅ Now it's just a dictionary
        print("frame_id: ", frame_id)

        doc_cmd = DomCommands.get_document(frame_id=frame_id)
        doc_result = await tab._connection_handler.execute_command(doc_cmd)
        doc_node_id = doc_result['result']['root']['nodeId']
        print(doc_result)



        await asyncio.sleep(10)

        await tab.close()

if __name__ == "__main__":
    asyncio.run(checkbox_radio_button())


number
., @, /, ?