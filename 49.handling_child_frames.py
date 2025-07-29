from pydoll.browser import Chrome
from pydoll.constants import By
from pydoll.exceptions import ElementNotFound
import asyncio
from pydoll.commands.runtime_commands import RuntimeCommands
from pydoll.commands.page_commands import PageCommands
from pydoll.commands.dom_commands import DomCommands
from pydoll.commands.input_commands import InputCommands

async def type_text(text, tab):
    for char in text:
        key_down = InputCommands.dispatch_key_event(
            type='keyDown', # This tells Chrome: “Simulate pressing this key down.” It starts the key event — like physically pressing a key on your keyboard.
            key=char, # key tells Chrome: Which key is being simulated(i.e being typed). If char = "j" → key="j" → the browser knows to treat this as "j".
            text=char, # This is the actual character that gets inserted into an input field (if it's focused).
            windows_virtual_key_code=ord(char.upper()),
            native_virtual_key_code=ord(char))

        key_up = InputCommands.dispatch_key_event(type='keyUp',key=char,text=char,windows_virtual_key_code=ord(char.upper()),native_virtual_key_code=ord(char))

        await tab._connection_handler.execute_command(key_down)
        await tab._connection_handler.execute_command(key_up)
        await asyncio.sleep(0.5)  # slight delay between keystrokes

async def focus_and_type(name_object_id, text, tab):
    focus_cmd = RuntimeCommands.call_function_on(
        object_id=name_object_id,
        function_declaration='function() { this.focus(); }',
        user_gesture=True,
        await_promise=False
    )
    await tab._connection_handler.execute_command(focus_cmd)
    await asyncio.sleep(0.2)
    await type_text(text, tab)

async def fill_inputs_in_iframe():
    async with Chrome() as browser:
        tab = await browser.start()

        await tab.go_to("https://letcode.in/frame")
        await asyncio.sleep(3)

        # STEP 1: Get root node of main document
        get_doc_cmd = DomCommands.get_document()
        get_doc_result = await tab._connection_handler.execute_command(get_doc_cmd)
        root_node_id = get_doc_result['result']['root']['nodeId']

        # STEP 2: Locate <iframe> in main page
        iframe_cmd = DomCommands.query_selector(selector="#firstFr", node_id=root_node_id)
        iframe_result = await tab._connection_handler.execute_command(iframe_cmd)
        iframe_node_id = iframe_result['result']['nodeId']

        # STEP 3: Get iframe's internal DOM root (contentDocument)
        desc_cmd = DomCommands.describe_node(node_id=iframe_node_id)
        desc_result = await tab._connection_handler.execute_command(desc_cmd)
        iframe_desc_node_id = desc_result['result']['node']['contentDocument']['nodeId']
        print("desc_result: ", desc_result)

        fname_cmd = DomCommands.query_selector(selector="input[placeholder='Enter name']", node_id=iframe_desc_node_id)
        lname_cmd = DomCommands.query_selector(selector="input[placeholder='Enter email']", node_id=iframe_desc_node_id)

        fname_result = await tab._connection_handler.execute_command(fname_cmd)
        lname_result = await tab._connection_handler.execute_command(lname_cmd)

        fname_node_id = fname_result['result']['nodeId']
        lname_node_id = lname_result['result']['nodeId']

        resolve_fname_cmd = DomCommands.resolve_node(node_id=fname_node_id)
        resolve_lname_cmd = DomCommands.resolve_node(node_id=lname_node_id)

        fname_obj = await tab._connection_handler.execute_command(resolve_fname_cmd)
        lname_obj = await tab._connection_handler.execute_command(resolve_lname_cmd)
        print(fname_obj)
        print(lname_obj)

        fname_obj_id = fname_obj['result']['object']['objectId']
        lname_obj_id = lname_obj['result']['object']['objectId']

        await focus_and_type(fname_obj_id, 'Joshua', tab)
        await focus_and_type(lname_obj_id, 'Echendu', tab)

        # Extract child <iframe> and give it an ID that references the child <iframe>
        child_iframe_cmd = DomCommands.query_selector(selector="iframe[src='innerframe']", node_id=iframe_desc_node_id)
        child_frame_result = await tab._connection_handler.execute_command(child_iframe_cmd)
        child_frame_root_node_id = child_frame_result['result']['nodeId']
        print(child_frame_result)

        # Extract the DOM structure from the child <iframe> and give it an ID that reference the DOM structure
        child_frame_desc_cmd = DomCommands.describe_node(node_id=child_frame_root_node_id)
        child_frame_desc = await tab._connection_handler.execute_command(child_frame_desc_cmd)
        child_frame_desc_node_id = child_frame_desc['result']['node']['contentDocument']['nodeId']

        # Extract the Email Input from the DOM structure and give it an ID that references the Email Input
        child_frame_email_cmd = DomCommands.query_selector(selector="input[placeholder='Enter email']", node_id=child_frame_desc_node_id)
        child_frame_email_result = await tab._connection_handler.execute_command(child_frame_email_cmd)
        child_frame_email_node_id = child_frame_email_result['result']['nodeId']
        print(child_frame_email_result)

        # Create a resolved environment and Extract the object ID
        child_frame_resolved_cmd = DomCommands.resolve_node(node_id=child_frame_email_node_id)
        child_frame_resolved = await tab._connection_handler.execute_command(child_frame_resolved_cmd)
        child_frame_object_id = child_frame_resolved['result']['object']['objectId']

        await focus_and_type(child_frame_object_id, "echendujosh@gmail.com", tab)
        # fname_obj_id = fname_obj[]
        await asyncio.sleep(10)

        await tab.close()

if __name__ == "__main__":
    asyncio.run(fill_inputs_in_iframe())

# 🧠 What Chrome Needs to Simulate a Keypress
# Chrome (via CDP and PyDoll) separates:

# What key you pressed (the physical key on the keyboard).

# What character was typed (the visual output, depending on modifier keys like Shift, Ctrl).

# 🔍 Breaking it Down:
# Let’s say you're simulating typing the lowercase "j".

# ✴️ windows_virtual_key_code = ord('J') = 74
# This tells Chrome:

# “Pretend the user physically pressed the J key.”

# It's always uppercase, because Chrome maps the physical keyboard layout this way.

# ✴️ native_virtual_key_code = ord('j') = 106
# This tells Chrome:

# “The character that appears should be ‘j’, not ‘J’.”

# It's what gets rendered in the text field.

# ✴️ Why not just use 'j' for both?
# Because:

# 'j' and 'J' are on the same physical key on the keyboard.

# Whether it's lowercase or uppercase depends on Shift key, which you’re not pressing.

# So you have to separate:

# The key that was hit ('J') 🧱

# From the character it produced ('j') 
