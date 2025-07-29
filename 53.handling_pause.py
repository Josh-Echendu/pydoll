from pydoll.browser import Chrome
from pydoll.constants import By
from pydoll.exceptions import ElementNotFound
import asyncio
from pydoll.commands.runtime_commands import RuntimeCommands
from pydoll.commands.page_commands import PageCommands
from pydoll.commands.dom_commands import DomCommands
from pydoll.commands.input_commands import InputCommands
from special_keys import all_characters, special_keys
import string

async def requires_shift(char):

    # We're going to use string.ascii_uppercase which gives: ABCDEFGHIJKLMNOPQRSTUVWXYZ
    if char in string.ascii_uppercase: # This checks if the character is a capital letter, like 'A', 'B', 'Z'
        
        return True
    
    if char in ")!@#$%^&*(_+{}|:\"`<>?":
        return True  # Known Shift-required characters
    return False


async def click_box(tab, box):
    coord_keys = ['x1', 'y1', 'x2', 'y2', 'x3', 'y3', 'x4', 'y4']
    bounds = dict(zip(coord_keys, box))

    # Compute element center (correctly)
    width = abs(bounds['x1'] - bounds['x2'])
    height = abs(bounds['y1'] - bounds['y4'])
    x = bounds['x1'] + width / 2
    y = bounds['y1'] + height / 2

    # left click: mousePressed + mouseReleased with button='right'
    cmd_press = InputCommands.dispatch_mouse_event(type='mousePressed',x=x,y=y,click_count=1,button='left',pointer_type='mouse')
    await tab._connection_handler.execute_command(cmd_press)

    cmd_release = InputCommands.dispatch_mouse_event(type='mouseReleased',x=x,y=y,click_count=1,button='left',pointer_type='mouse')
    await tab._connection_handler.execute_command(cmd_release)

async def querySelector(tab, node_id, selector):
    cmd = DomCommands.query_selector(selector=selector, node_id=node_id)
    result = await tab._connection_handler.execute_command(cmd)
    print(result)
    node_id = result['result']['nodeId']
    return node_id


async def resolve(tab, node_id):
    cmd = DomCommands.resolve_node(node_id=node_id)
    resolve = await tab._connection_handler.execute_command(cmd)
    obj = resolve['result']['object']['objectId'] 
    
    cmd = RuntimeCommands.call_function_on(function_declaration="""function() { this.focus(); }""",object_id=obj,user_gesture=True,await_promise=False)
    await tab._connection_handler.execute_command(cmd)
    return

async def special(tab, key, pause=None):
    key_info = special_keys[key]

    down_cmd = InputCommands.dispatch_key_event(
        type='keyDown',
        key=key,
        text=None,
        code=key_info['code'],
        windows_virtual_key_code=key_info['keyCode'],
        native_virtual_key_code=key_info['native_virtual_key_code'])

    up_cmd = InputCommands.dispatch_key_event(
        type='keyUp',
        key=key,
        text=None,
        code=key_info['code'],
        windows_virtual_key_code=key_info['keyCode'],
        native_virtual_key_code=key_info['native_virtual_key_code'])

    await tab._connection_handler.execute_command(down_cmd)
    await tab._connection_handler.execute_command(up_cmd)

    if pause:
        await asyncio.sleep(pause)

async def send_key(key, tab, shift=False, text=None):
    key_info = all_characters[key]

    if shift:
        shift_down_cmd = InputCommands.dispatch_key_event(
            type='keyDown',
            key='Shift',
            text=text,
            code="ShiftLeft",
            windows_virtual_key_code=16,
            native_virtual_key_code=16,
        )
        j = await tab._connection_handler.execute_command(shift_down_cmd)
        print('down: ', j)

    key_down_cmd = InputCommands.dispatch_key_event(
        type='keyDown',
        key=key,
        text=key, 
        code=key_info['code'], 
        unmodified_text=key_info['unmodified_text'], 
        windows_virtual_key_code=key_info['keyCode'],
        native_virtual_key_code=key_info['native_virtual_key_code']
    )
    key_up_cmd = InputCommands.dispatch_key_event(
        type='keyUp',
        key=key,
        text=key,
        code=key_info['code'],
        unmodified_text=key_info['unmodified_text'],
        windows_virtual_key_code=key_info['keyCode'],
        native_virtual_key_code=key_info['native_virtual_key_code'],
    )

    if shift:
        shift_up_cmd = InputCommands.dispatch_key_event(
            type='keyUp',
            key='Shift',
            text=text,
            code='ShiftLeft',
            native_virtual_key_code=16,
            windows_virtual_key_code=16
        )
        k = await tab._connection_handler.execute_command(shift_up_cmd)
        print('up: ', k)
    await tab._connection_handler.execute_command(key_down_cmd)
    await tab._connection_handler.execute_command(key_up_cmd)
    await asyncio.sleep(0.3)

async def fill_inputs_in_iframe():
    async with Chrome() as browser:
        tab = await browser.start()

        await tab.go_to("https://tutorialsninja.com/demo/index.php?route=account/register")

        await asyncio.sleep(3)

        doc_cmd = DomCommands.get_document()
        main_doc = await tab._connection_handler.execute_command(doc_cmd)
        main_doc_node_id = main_doc['result']['root']['nodeId']
        print(main_doc)

        fname_node_id = await querySelector(tab, main_doc_node_id, selector='#input-firstname')

        await resolve(tab, fname_node_id)
        
        for ch in 'Ec#$%^&':
            result = await requires_shift(ch)
            await send_key(ch, tab, shift=result)

        await special(tab, 'Tab', pause=2)

        for ch in 'joshua***#@!':
            result = await requires_shift(ch)
            await send_key(ch, tab, shift=result)

        await special(tab, 'Tab', pause=2)

        for ch in 'echen@#$dujosh@gmail.com':
            result = await requires_shift(ch)
            await send_key(ch, tab, shift=result)

        await special(tab, 'Tab', pause=2)

        for ch in '0906@#?"">3938743':
            result = await requires_shift(ch)
            await send_key(ch, tab, shift=result)

        await special(tab, 'Tab',  pause=2)

        for ch in "12345":
            result = await requires_shift(ch)
            await send_key(ch, tab, shift=result)

        await special(tab, 'Tab', pause=2)

        for ch in "12345":
            result = await requires_shift(ch)
            await send_key(ch, tab, shift=result)

        await special(tab,'Tab', pause=2)

        await special(tab, 'ArrowLeft', pause=0.5)

        await special(tab,'Tab', pause=0.5)

        await special(tab,'Tab', pause=0.5)

        # Checkbox node_id
        checkbox_node_id = await querySelector(tab, main_doc_node_id, selector="input[value='1'][name='agree']")

        # Get the coordinate of the checkbox
        box_cmd = DomCommands.get_box_model(node_id=checkbox_node_id)
        result1 = await tab._connection_handler.execute_command(box_cmd)
        box = result1['result']['model']['content']

        # click the Check box
        await click_box(tab, box)
        
        await special(tab,'Tab', pause=2)

        continue_box_id = await querySelector(tab, main_doc_node_id, selector="input[value='Continue']")
        box_cmd1 = DomCommands.get_box_model(node_id=continue_box_id)
        result1 = await tab._connection_handler.execute_command(box_cmd1)
        box1 = result1['result']['model']['content']

        await click_box(tab, box1)

        await asyncio.sleep(7)

        await tab.close()

if __name__ == "__main__":
    asyncio.run(fill_inputs_in_iframe())
