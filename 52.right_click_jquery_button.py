from pydoll.browser import Chrome
from pydoll.constants import By
from pydoll.exceptions import ElementNotFound
import asyncio
from pydoll.commands.runtime_commands import RuntimeCommands
from pydoll.commands.page_commands import PageCommands
from pydoll.commands.dom_commands import DomCommands
from pydoll.commands.input_commands import InputCommands

async def bounding_box(box):
    coord_keys = ['x1', 'y1', 'x2', 'y2', 'x3', 'y3', 'x4', 'y4']
    bounds = dict(zip(coord_keys, box))

    # Compute element center (correctly)
    width = abs(bounds['x1'] - bounds['x2'])
    height = abs(bounds['y1'] - bounds['y4'])
    center_x = bounds['x1'] + width / 2
    center_y = bounds['y1'] + height / 2

    return center_x, center_y

async def run():
    async with Chrome() as browser:
        tab = await browser.start()

        await tab.go_to("https://swisnl.github.io/jQuery-contextMenu/demo.html")

        await asyncio.sleep(3)

        main_page_doc = DomCommands.get_document()
        main_doc_result = await tab._connection_handler.execute_command(main_page_doc)
        print(main_doc_result)
        main_doc_node_id = main_doc_result['result']['root']['nodeId']

        button_cmd = DomCommands.query_selector(selector=".context-menu-one.btn.btn-neutral", node_id=main_doc_node_id)
        button = await tab._connection_handler.execute_command(button_cmd)
        button_node_id = button['result']['nodeId']

        # Get box model
        box_cmd = DomCommands.get_box_model(node_id=button_node_id)
        box_result = await tab._connection_handler.execute_command(box_cmd)
        box = box_result['result']['model']['content']

        bounds = await bounding_box(box)
        center_x = bounds[0]
        center_y = bounds[1]

        # Right click: mousePressed + mouseReleased with button='right'
        cmd_press = InputCommands.dispatch_mouse_event(
            type='mousePressed',
            x=center_x,
            y=center_y,
            click_count=1,
            button='right',
            pointer_type='mouse'
        )
        await tab._connection_handler.execute_command(cmd_press)

        cmd_release = InputCommands.dispatch_mouse_event(
            type='mouseReleased',
            x=center_x,
            y=center_y,
            click_count=1,
            button='right',
            pointer_type='mouse'
        )
        await tab._connection_handler.execute_command(cmd_release)
        await asyncio.sleep(3)

        edit_cmd = DomCommands.query_selector(
            selector="li[class='context-menu-item context-menu-icon context-menu-icon-edit'] span",
            node_id=main_doc_node_id
        )
        edit = await tab._connection_handler.execute_command(edit_cmd)
        edit_node_id = edit['result']['nodeId']

        box_cmd = DomCommands.get_box_model(node_id=edit_node_id)
        box_result = await tab._connection_handler.execute_command(box_cmd) 
        box = box_result['result']['model']['content']
        print(box)

        bounds1 = await bounding_box(box)
        print(bounds1)

        x = bounds1[0]
        y = bounds1[1]

                # Right click: mousePressed + mouseReleased with button='right'
        cmd_press = InputCommands.dispatch_mouse_event(
            type='mousePressed',
            x=x,
            y=y,
            click_count=1,
            button='right',
            pointer_type='mouse'
        )
        await tab._connection_handler.execute_command(cmd_press)

        cmd_release = InputCommands.dispatch_mouse_event(
            type='mouseReleased',
            x=x,
            y=y,
            click_count=1,
            button='right',
            pointer_type='mouse'
        )
        await tab._connection_handler.execute_command(cmd_release)
        await asyncio.sleep(3)

        await asyncio.sleep(7)

        await tab.close()

asyncio.run(run())

# from pydoll.browser import Chrome
# from pydoll.constants import By
# from pydoll.exceptions import ElementNotFound
# import asyncio
# from pydoll.commands.runtime_commands import RuntimeCommands
# from pydoll.commands.page_commands import PageCommands
# from pydoll.commands.dom_commands import DomCommands
# from pydoll.commands.input_commands import InputCommands


# async def run():
#     async with Chrome() as browser:
#         tab = await browser.start()

#         await tab.go_to("https://swisnl.github.io/jQuery-contextMenu/demo.html")

#         await asyncio.sleep(3)

#         main_page_doc = DomCommands.get_document()
#         main_doc_result = await tab._connection_handler.execute_command(main_page_doc)
#         print(main_doc_result)
#         main_doc_node_id = main_doc_result['result']['root']['nodeId']

#         button_cmd = DomCommands.query_selector(selector="a[href='#example-html-simple-context-menu']", node_id=main_doc_node_id)
#         button = await tab._connection_handler.execute_command(button_cmd)
#         button_node_id = button['result']['nodeId']

#         resolv_but_cmd = DomCommands.resolve_node(node_id=button_node_id)
#         resolv_but = await tab._connection_handler.execute_command(resolv_but_cmd)
#         print(resolv_but)
#         obj_id = resolv_but['result']['object']['objectId']
#         print(obj_id)

#         cmd = RuntimeCommands.call_function_on(
#             user_gesture=True,
#             function_declaration="function() { this.focus(); }",
#             object_id=obj_id,
#             await_promise=False
#         )
#         await asyncio.sleep(7)
#         await tab._connection_handler.execute_command(cmd)

#         await tab.close()

# asyncio.run(run())

