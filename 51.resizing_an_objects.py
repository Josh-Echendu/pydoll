import asyncio
import time
from pydoll.session import launch
from pydoll.commands.page_commands import PageCommands
from pydoll.commands.dom_commands import DomCommands
from pydoll.commands.input_commands import InputCommands

async def run():
    browser = await launch(headless=False)
    tab = browser.tabs[0]

    # Step 1: Go to the target URL
    await tab.execute(PageCommands.navigate(url="https://jqueryui.com/resizable/"))
    await tab.wait_until_loaded()
    time.sleep(3)

    # Step 2: Get root node
    root = await tab.execute(DomCommands.get_document())
    root_node_id = root["root"]["nodeId"]

    # Step 3: Get iframe node
    iframe_node = await tab.execute(DomCommands.query_selector(
        selector="iframe.demo-frame", node_id=root_node_id
    ))
    iframe_node_id = iframe_node["nodeId"]

    # Step 4: Get iframe frameId
    desc = await tab.execute(DomCommands.describe_node(node_id=iframe_node_id))
    frame_id = desc["node"]["frameId"]

    # Step 5: Get document inside iframe
    iframe_doc = await tab.execute(DomCommands.get_document(frame_id=frame_id))
    iframe_root_id = iframe_doc["root"]["nodeId"]

    # Step 6: Find the resize handle node
    handle_node = await tab.execute(DomCommands.query_selector(
        selector="div#resizable > div.ui-resizable-se", node_id=iframe_root_id
    ))
    handle_node_id = handle_node["nodeId"]

    # Step 7: Get objectId for handle
    resolved = await tab.execute(DomCommands.resolve_node(node_id=handle_node_id))
    object_id = resolved["object"]["objectId"]

    # Step 8: Get position
    box = await tab.execute(DomCommands.get_box_model(object_id=object_id))
    quad = box["model"]["content"]
    x = (quad[0] + quad[4]) / 2
    y = (quad[1] + quad[5]) / 2

    # Step 9: Simulate mouse drag
    await tab._connection_handler.execute_command(InputCommands.dispatch_mouse_event(
        type="mousePressed", x=x, y=y, button="left", click_count=1, pointer_type="mouse"
    ))

    await tab._connection_handler.execute_command(InputCommands.dispatch_mouse_event(
        type="mouseMoved", x=x + 100, y=y - 50, button="left", click_count=1, pointer_type="mouse"
    ))

    await tab._connection_handler.execute_command(InputCommands.dispatch_mouse_event(
        type="mouseReleased", x=x + 100, y=y - 50, button="left", click_count=1, pointer_type="mouse"
    ))

    time.sleep(5)
    await tab.close()
    await browser.close()

asyncio.run(run())
