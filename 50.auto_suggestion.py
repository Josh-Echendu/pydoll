from pydoll.browser import Chrome
from pydoll.constants import By
from pydoll.exceptions import ElementNotFound
import asyncio
from pydoll.commands.runtime_commands import RuntimeCommands
from pydoll.commands.page_commands import PageCommands
from pydoll.commands.dom_commands import DomCommands
from pydoll.commands.input_commands import InputCommands


async def fill_inputs_in_iframe():
    async with Chrome() as browser:
        tab = await browser.start()

        await tab.go_to("https://www.makemytrip.com/")

        await asyncio.sleep(3)

        doc_cmd = DomCommands.get_document()
        main_doc = await tab._connection_handler.execute_command(doc_cmd)
        main_doc_node_id = main_doc['result']['root']['nodeId']
        print(main_doc)

        press_up_cmd = InputCommands.dispatch_mouse_event(type='mousePressed',click_count=1,pointer_type='mouse',x=0,y=0,button='left')
        rel_up_cmd = InputCommands.dispatch_mouse_event(type='mouseReleased',click_count=1,pointer_type='mouse',x=0,y=0,button='left')

        await tab._connection_handler.execute_command(press_up_cmd)
        await tab._connection_handler.execute_command(rel_up_cmd)

        from_cmd = DomCommands.query_selector(selector = "label[for='fromCity'] span[class='lbl_input appendBottom10']", node_id=main_doc_node_id)
        from_icon = await tab._connection_handler.execute_command(from_cmd)
        from_node_id = from_icon['result']['nodeId']
        print("from: ", from_icon)
        
        await asyncio.sleep(5)
        resolve_from_cmd = DomCommands.resolve_node(node_id=from_node_id)
        resolved_from = await tab._connection_handler.execute_command(resolve_from_cmd)
        print(resolved_from)
        from_obj_id = resolved_from['result']['object']['objectId']

        from_func_cmd = RuntimeCommands.call_function_on(object_id = from_obj_id,function_declaration="function() { this.click(); }",user_gesture=True,await_promise=False)
        await tab._connection_handler.execute_command(from_func_cmd)

        focus_cmd2 = DomCommands.resolve_node(node_id=main_doc_node_id)
        focus_obj = await tab._connection_handler.execute_command(focus_cmd2)
        print(focus_obj)
        focus_obj_id = focus_obj['result']['object']['objectId']

        await tab._connection_handler.execute_command(RuntimeCommands.call_function_on(object_id=focus_obj_id,user_gesture=True,function_declaration="function() { this.focus(); }",await_promise=False))
        key = 'g'
        await tab._connection_handler.execute_command(InputCommands.dispatch_key_event(key=key,text=key,type='keyDown', windows_virtual_key_code=ord(key.upper()), native_virtual_key_code=ord(key)))
        await tab._connection_handler.execute_command(InputCommands.dispatch_key_event(key=key,text=key,type='keyUp', windows_virtual_key_code=ord(key.upper()), native_virtual_key_code=ord(key)))

        for _ in range(3):
            # special_keys = {"ArrowDown": 40, "ArrowUp": 38, "ArrowLeft": 37, "ArrowRight": 39, "Enter": 13, "Escape": 27, "Tab": 9}
            down_cmd = InputCommands.dispatch_key_event(
                type="keyDown",
                key='ArrowDown', 
                text='', # arrowDown is a special key, Special keys don’t generate visible characters in input fields.
                windows_virtual_key_code=40, # ascii value of "Arrowdown"
                native_virtual_key_code=40 # ascii value of "ArrowDown"
            )

            up_cmd = InputCommands.dispatch_key_event(
                type="keyUp",
                key='ArrowDown', 
                text='', # arrowDown is a special key, Special keys don’t generate visible characters in input fields.
                windows_virtual_key_code=40, # ascii value of "Arrowdown"
                native_virtual_key_code=40 # ascii value of "ArrowDown"
            )
            await tab._connection_handler.execute_command(down_cmd)
            await tab._connection_handler.execute_command(up_cmd)
            await asyncio.sleep(1)


        await asyncio.sleep(7)

        await tab.close()

if __name__ == "__main__":
    asyncio.run(fill_inputs_in_iframe())


# ✅ 1. text="" for special keys
# Special keys don’t generate visible characters in input fields.

# | Key           | `key`         | `text` |
# | ------------- | ------------- | ------ |
# | `"a"`         | `"a"`         | `"a"`  |
# | `"ArrowDown"` | `"ArrowDown"` | `""`   |
# | `"Enter"`     | `"Enter"`     | `""`   |
# | `"Tab"`       | `"Tab"`       | `""`   |
# | `"b"`         |  `"b"`        | `"a"`  |


# ✅ Correct Way to Send Special Keys like "ArrowDown", "Enter", "Escape":
# You do not use ord().

# You must hardcode the correct virtual key code. For "ArrowDown":

# | Field                      | Value         |
# | -------------------------- | ------------- |
# | `key`                      | `"ArrowDown"` |
# | `text`                     | `""`          |
# | `windows_virtual_key_code` | `40`          |
# | `native_virtual_key_code`  | `40`          |


# | Parameter                  | Meaning                                                                 |
# | -------------------------- | ----------------------------------------------------------------------- |
# | `windows_virtual_key_code` | The **physical key** code based on a **Windows keyboard layout**        |
# | `native_virtual_key_code`  | The **physical key** code based on your OS — e.g., **Mac** native codes |
# | Parameter                  | Value | Why                                                |

# 🔡 You type 'a' (lowercase):
# | -------------------------- | ----- | -------------------------------------------------- |
# | `windows_virtual_key_code` | `65`  | You're pressing the **'A' key** on the keyboard    |
# | `native_virtual_key_code`  | `97`  | `'a'` is ASCII 97, and on macOS it reflects output |



# 🔠 You type 'A' (uppercase, using Shift):
# | Parameter                  | Value | Why                                               |
# | -------------------------- | ----- | ------------------------------------------------- |
# | `windows_virtual_key_code` | `65`  | Still the **'A' key** physically pressed          |
# | `native_virtual_key_code`  | `65`  | `'A'` is ASCII 65, which is the actual typed char |


# In the dispatch_key_event payload, the code field refers to the physical location of the key on the keyboard — not the character it produces.