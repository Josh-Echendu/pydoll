from pydoll.browser import Chrome
from pydoll.commands.page_commands import PageCommands
from pydoll.commands.runtime_commands import RuntimeCommands
import asyncio

async def create_sanbox_isolated_world(frame_id: int, world_name: str, tab):

    # this means: I want a fresh, isolated JavaScript world inside a specific iframe, where I can run custom code.
    create_world_cmd = PageCommands.create_isolated_world(
        frame_id=frame_id, # Tells PyDoll which iframe to target.
        world_name=world_name, # You're giving a name to the isolated JavaScript world you're creating.
        grant_universal_access=True # Please allow this isolated world to access all the document’s features — like scripts, styles, DOM — even across frames if needed.
    )

    # You’ve now successfully created a sandboxed JavaScript environment inside the iframe, and Chrome gives you an ID for it.
    world_response = await tab._connection_handler.execute_command(create_world_cmd)

    # Extracted the unique identifier for that sandbox given to you by Chrome
    context_id = world_response["result"]["executionContextId"]  # ✅ correct access

    return context_id

async def evalute_javascript(expression: str, context_id: int, tab):
    
    # Step 3: Evaluate JS inside iframe
    eval_cmd = RuntimeCommands.evaluate(
        expression=expression,
        return_by_value=True,

        # When we build the JavaScript command (evaluate), we include that same context_id so the code will run inside the correct iframe sandbox we just created — not in the main page or a different frame.
        context_id=context_id
    )
    result = await tab._connection_handler.execute_command(eval_cmd)
    print("✅ JS Result:", result)



async def checkbox_radio_button():
    async with Chrome() as browser:
        tab = await browser.start()

        await tab.go_to("https://letcode.in/frame/")
        await asyncio.sleep(3)

        # Step 1: Get frame tree
        frame_tree_cmd = PageCommands.get_frame_tree()

        # Actually sends the above command to the browser, waits for the response, and stores it in frame_tree.
        frame_tree = await tab._connection_handler.execute_command(frame_tree_cmd)
        print(frame_tree)
        outer_frame = frame_tree['result']['frameTree']['childFrames'][0]
        outer_frame_id = outer_frame['frame']['id']

        # create a new isolated world for an iframe and extract the context_id
        context_id =  await create_sanbox_isolated_world(outer_frame_id, 'frame_tree_sandbox', tab) 
        
        # javascript expression
        expression_name="document.querySelector('input[placeholder=\"Enter name\"]').value = 'Echendu'"

        # Evaluate JS inside iframe
        await evalute_javascript(expression_name, context_id, tab)

        # javascript expression
        expression_email="document.querySelector('input[placeholder=\"Enter email\"]').value = 'Echendu@gmail.com'"

        # Evaluate JS inside iframe
        await evalute_javascript(expression_email, context_id, tab)

        child_frame = frame_tree['result']['frameTree']['childFrames'][0]['childFrames'][0]
        print("child: ", child_frame)

        # extract the frame ID
        child_frame_id = child_frame['frame']['id']

        context_id2 = await create_sanbox_isolated_world(child_frame_id, 'any_name_bro', tab)

        js_expression_lname ="document.querySelector('input[placeholder=\"Enter email\"]').value = 'joshua'"

        await evalute_javascript(js_expression_lname, context_id2, tab)

        await asyncio.sleep(30)
        await tab.close()

if __name__ == "__main__":
    asyncio.run(checkbox_radio_button())


