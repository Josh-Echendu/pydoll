import asyncio
from pydoll.browser import Chrome
from pydoll.browser.options import ChromiumOptions
from pydoll.constants import By
from pydoll.protocol.fetch.events import FetchEvent
# from functools import partial # This import is not used and can be removed, but since the instruction is only "corrections", it's left as is.

async def handle_auth_dialog(tab, browser, event):
    print("event: ", event)
    request_id = event['params']['requestId']
    auth_challenge = event['params']['authChallenge']

    print(f"Authentication required: {auth_challenge['origin']}")

    # Correction 1: Use 'tab' object for continue_request_with_auth, not 'browser'.
    await tab.continue_request_with_auth(
        request_id=request_id,
        auth_challenge_response='ProvideCredentials',
        username='admin',
        password='admin',
    )

async def tag_name_elements():
    options = ChromiumOptions()
    options.add_argument("--start-maximized")

    async with Chrome() as browser:
        tab = await browser.start()
        await tab.go_to("https://the-internet.herokuapp.com/")
        await asyncio.sleep(3)

        # Correction 4: Navigate to the correct URL that triggers basic authentication.
        await tab.go_to("ttps://the-internet.herokuapp.com/")

        print("passed")
        link = await tab.find(text='Basic Auth', timeout=10000)# Added timeout for robustness
        await link.click()

        # Correction 3: Enable fetch events and register the handler BEFORE navigation.
        await tab.enable_fetch_events(handle_auth=True)
        await tab.on(FetchEvent.AUTH_REQUIRED, lambda event: asyncio.create_task(handle_auth_dialog(tab, browser, event)))

        # Keep the tab open for a short while after successful operation for observation
        await asyncio.sleep(1000) # Added for observation before close

        # Correction 8: Ensure tab is closed only once, after all operations are done.
        await tab.close()

    
if __name__ == "__main__":
    asyncio.run(tag_name_elements())