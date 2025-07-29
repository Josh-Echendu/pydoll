from pydoll.browser import Chrome
from pydoll.constants import By
from pydoll.exceptions import ElementNotFound
import asyncio
from pydoll.commands.runtime_commands import RuntimeCommands
from pydoll.commands.page_commands import PageCommands
from pydoll.commands.dom_commands import DomCommands
from pydoll.commands.input_commands import InputCommands


async def run():
    async with Chrome() as browser:
        tab = await browser.start()

        await tab.go_to("https://jqueryui.com/resizable/")

        await asyncio.sleep(3)

        main_page_doc = DomCommands.get_document()
        main_doc_result = await tab._connection_handler.execute_command(main_page_doc)
        print(main_doc_result)
        main_doc_node_id = main_doc_result['result']['root']['nodeId']

        iframe_cmd = DomCommands.query_selector(selector='.demo-frame', node_id=main_doc_node_id)
        iframe_result = await tab._connection_handler.execute_command(iframe_cmd)
        print(iframe_result)
        iframe_node_id = iframe_result['result']['nodeId']

        iframe_desc_cmd = DomCommands.describe_node(node_id=iframe_node_id)
        iframe_desc_result = await tab._connection_handler.execute_command(iframe_desc_cmd)
        print(iframe_desc_result)
        frame_id = iframe_desc_result['result']['node']['contentDocument']['nodeId']
        print(frame_id)

        cmd = DomCommands.query_selector(selector='#resizable', node_id=frame_id)
        cmd_result = await tab._connection_handler.execute_command(cmd)
        cmd_node_id = cmd_result['result']['nodeId']

        box_cmd = DomCommands.get_box_model(node_id=cmd_node_id)
        box_result = await tab._connection_handler.execute_command(box_cmd) 
        box = box_result['result']['model']['content']
        print(box)
        coord_keys = ['x1', 'y1', 'x2', 'y2', 'x3', 'y3', 'x4', 'y4']
        bounds = dict(zip(coord_keys, box))
        print(bounds)

        x = bounds['x3']
        y = bounds['y3']

    # Step 9: Simulate mouse drag
        await tab._connection_handler.execute_command(InputCommands.dispatch_mouse_event(
            type="mousePressed", x=x, y=y, button="left", click_count=1, pointer_type="mouse"
        ))

        await tab._connection_handler.execute_command(InputCommands.dispatch_mouse_event(
            type="mouseMoved", x=x + 100, y=y, button="left", click_count=1, pointer_type="mouse"
        ))

        await tab._connection_handler.execute_command(InputCommands.dispatch_mouse_event(
            type="mouseReleased", x=x + 100, y=y, button="left", click_count=1, pointer_type="mouse"
        ))
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

#         await tab.go_to("https://jqueryui.com/resizable/")

#         await asyncio.sleep(3)

#         main_page_doc = DomCommands.get_document()
#         main_doc_result = await tab._connection_handler.execute_command(main_page_doc)
#         print(main_doc_result)
#         main_doc_node_id = main_doc_result['result']['root']['nodeId']

#         iframe_cmd = DomCommands.query_selector(selector='.demo-frame', node_id=main_doc_node_id)
#         iframe_result = await tab._connection_handler.execute_command(iframe_cmd)
#         print(iframe_result)
#         iframe_node_id = iframe_result['result']['nodeId']

#         iframe_desc_cmd = DomCommands.describe_node(node_id=iframe_node_id)
#         iframe_desc_result = await tab._connection_handler.execute_command(iframe_desc_cmd)
#         print(iframe_desc_result)
#         frame_id = iframe_desc_result['result']['node']['frameId']
#         print(frame_id)

#         page_cmd  = PageCommands.create_isolated_world(
#             frame_id=frame_id,
#             grant_universal_access=True,
#             world_name='josh'
#         )
#         context = await tab._connection_handler.execute_command(page_cmd)
#         context_id = context['result']['executionContextId']
#         print(context)

#         script = """
#         (() => {
#             const el = document.querySelector('#resizable');
#             const rect = el.getBoundingClientRect();
#             return {
#                 x: rect.x + rect.width/2,
#                 y: rect.y + rect.height/2,
#             };
#         })()
#         """

#         js_cmd = RuntimeCommands.evaluate(
#             context_id=context_id,
#             return_by_value=True,
#             expression=script,
#         )

#         result = await tab._connection_handler.execute_command(js_cmd)
#         print(result)
#         x = result['result']['result']['value']['x']
#         y = result['result']['result']['value']['y']


#     # Step 9: Simulate mouse drag
#         await tab._connection_handler.execute_command(InputCommands.dispatch_mouse_event(
#             type="mousePressed", x=x, y=y, button="left", click_count=1, pointer_type="mouse"
#         ))

#         await tab._connection_handler.execute_command(InputCommands.dispatch_mouse_event(
#             type="mouseMoved", x=x + 100, y=y - 50, button="left", click_count=1, pointer_type="mouse"
#         ))

#         await tab._connection_handler.execute_command(InputCommands.dispatch_mouse_event(
#             type="mouseReleased", x=x + 100, y=y - 50, button="left", click_count=1, pointer_type="mouse"
#         ))
#         await tab.close()

# asyncio.run(run())
