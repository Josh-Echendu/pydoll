from pydoll.commands.dom_commands import DomCommands
get_doc_cmd = DomCommands.get_document()
get_doc_cmd["sessionId"] = popup_session_id
doc = await tab._connection_handler.execute_command(get_doc_cmd)

node_id = doc["result"]["root"]["nodeId"]

query_cmd = DomCommands.query_selector(
    node_id=node_id,
    selector="h3"
)
query_cmd["sessionId"] = popup_session_id
result = await tab._connection_handler.execute_command(query_cmd)


##########################################################################
from pydoll.commands.input_commands import dispatch_key_event

key_cmd = dispatch_key_event(
    type="keyDown",
    windows_virtual_key_code=65,  # A
    code="KeyA",
    key="a",
    text="a"
)

key_cmd["sessionId"] = popup_session_id
await tab._connection_handler.execute_command(key_cmd)


##########################################################
✅ Commands that require sessionId injection:
These must have command["sessionId"] = your_session_id added manually:

| Command Type         | Example Commands                                                          |
| -------------------- | ------------------------------------------------------------------------- |
| **DOM Commands**     | `DomCommands.get_document()`, `query_selector()`, `resolve_node()`        |
| **Runtime Commands** | `RuntimeCommands.evaluate()`, `call_function_on()`                        |
| **Input Events**     | `dispatch_mouse_event`, `dispatch_key_event`, `dispatch_touch_event`      |
| **Page Commands**    | `PageCommands.capture_screenshot()`, `navigate()` (if manually triggered) |
| **Overlay Commands** | `HighlightNode`, `hideHighlight` (if used in debugging)                   |

