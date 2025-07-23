from pydoll.browser import Chrome
from pydoll.constants import By
from pydoll.exceptions import ElementNotFound
import asyncio
from pydoll.commands.runtime_commands import RuntimeCommands
from pydoll.commands.page_commands import PageCommands
from pydoll.commands.dom_commands import DomCommands
from pydoll.commands.input_commands import InputCommands

async def find_target_frame(tree):
    if tree['frame'].get("name") == 'iframeResult':
        print('Result: ', tree['frame'])
        return tree['frame']
    for child in tree.get('childFrames', []):
        result = await find_target_frame(child)
        if result:
            return result
    return None


async def center(bounds):
    width = abs(bounds['x1'] - bounds['x2'])
    height = abs(bounds['y1'] - bounds['y4'])

    center_x = bounds['x1'] + width/2
    center_y = bounds['y1'] + height/2

    return center_x, center_y

async def checkbox_radio_button():
    async with Chrome() as browser:
        tab = await browser.start()

        await tab.go_to("https://www.w3schools.com/html/tryit.asp?filename=tryhtml5_draganddrop")
        await asyncio.sleep(3)

        # STEP 1: Get the root node of the main document:
        get_doc_cmd = DomCommands.get_document()
        get_doc_result = await tab._connection_handler.execute_command(get_doc_cmd)
        root_node_id = get_doc_result['result']['root']['nodeId']
        print(get_doc_result)
        
        # STEP 2: Find the <iframe> inside the main document: This confirms the iframe is part of the main DOM, and query_selector gives it a nodeId.
        iframe_cmd = DomCommands.query_selector(selector="#iframeResult", node_id=root_node_id)
        iframe_result = await tab._connection_handler.execute_command(iframe_cmd)
        iframe_node_id = iframe_result['result']['nodeId']
        print(iframe_result)

        # STEP 3: Tell the browser, Hey browser, please give me a deep description of this iframe element — not just its tag, but what it contains.
        desc_cmd = DomCommands.describe_node(node_id=iframe_node_id)
        desc_result = await tab._connection_handler.execute_command(desc_cmd)
        iframe_root_node_id = desc_result['result']['node']['contentDocument']['nodeId']
        print("josh: ", desc_result)

        drag_cmd = DomCommands.query_selector(selector="#img1", node_id=iframe_root_node_id)
        drop_cmd = DomCommands.query_selector(selector='#div1', node_id=iframe_root_node_id)

        drag_result = await tab._connection_handler.execute_command(drag_cmd)
        drop_result = await tab._connection_handler.execute_command(drop_cmd)
        print('drag_result: ',drag_result)
        print('drop_result: ',drop_result)

        drag_node_id = drag_result['result']['nodeId']
        drop_node_id = drop_result['result']['nodeId']

        drag_box_cmd = DomCommands.get_box_model(node_id=drag_node_id)
        drop_box_cmd = DomCommands.get_box_model(node_id=drop_node_id)

        drag_box = await tab._connection_handler.execute_command(drag_box_cmd)
        drop_box = await tab._connection_handler.execute_command(drop_box_cmd)
        
        print('drag_box: ', drag_box)
        print()
        print('drop_box: ', drop_box)

        drag_quad = drag_box['result']['model']['content']
        drop_quad = drop_box['result']['model']['content']
        coord_keys = ['x1', 'y1', 'x2', 'y2', 'x3', 'y3', 'x4', 'y4']

        drag_bounds = dict(zip(coord_keys, drag_quad))
        drop_bounds = dict(zip(coord_keys, drop_quad))

        drag_coordinates = asyncio.create_task(center(drag_bounds))
        drop_coordinates = asyncio.create_task(center(drop_bounds))

        drag_coordinates = await drag_coordinates
        drop_coordinates = await drop_coordinates

        drag_x = drag_coordinates[0]
        drag_y = drag_coordinates[1]

        drop_x = drop_coordinates[0]
        drop_y = drop_coordinates[1]

        mov_cmd = InputCommands.dispatch_mouse_event(type='mouseMoved', x=drag_x, y=drag_y, pointer_type='mouse', button='none')
        pres_cmd = InputCommands.dispatch_mouse_event(type='mousePressed', x=drag_x, y=drag_y, pointer_type='mouse', button='left', click_count=1)
        mov1_cmd = InputCommands.dispatch_mouse_event(type='mouseMoved', x=drop_x, y=drop_y, pointer_type='mouse', button='left')
        releas_cmd = InputCommands.dispatch_mouse_event(type='mouseReleased', x=drop_x, y=drop_y, pointer_type='mouse', button='left', click_count=1)

        await tab._connection_handler.execute_command(mov_cmd)
        await tab._connection_handler.execute_command(pres_cmd)
        await tab._connection_handler.execute_command(mov1_cmd)
        await tab._connection_handler.execute_command(releas_cmd)
        await asyncio.sleep(10)

        await tab.close()

if __name__ == "__main__":
    asyncio.run(checkbox_radio_button())
