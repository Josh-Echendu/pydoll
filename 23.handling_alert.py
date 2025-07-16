import asyncio
from pydoll.browser import Chrome
from pydoll.browser.options import ChromiumOptions
from pydoll.constants import By

# event: event data about the dialog opening.
async def dialog_handler(tab, event):

    # event:  {'method': 'Page.javascriptDialogOpening', 'params': {'url': 'https://the-internet.herokuapp.com/javascript_alerts', 'message': 'I am a JS Alert', 'type': 'alert', 'hasBrowserHandler': True, 'defaultPrompt': ''}}
    print('event: ', event)

    # Checks asynchronously if a dialog (alert/confirm/prompt) is currently present on the page.
    if await tab.has_dialog():

        # If a dialog exists, this fetches the text message shown in the dialog (e.g., alert text).
        message = await tab.get_dialog_message()
        print(f"Dialog message: {message}")
        
        # Accepts the dialog (clicks "OK" or "Confirm").
        await tab.handle_dialog(accept=True)# Accept the dialog

async def tag_name_elements():
    options = ChromiumOptions()
    options.add_argument("--start-maximized")

    async with Chrome() as browser:
        tab = await browser.start()
        await tab.go_to("https://the-internet.herokuapp.com/")
        await asyncio.sleep(3)

        await (await tab.find(text='JavaScript Alerts')).click()
        current_main = "https://the-internet.herokuapp.com/javascript_alerts"
        current_url_coroutine = await tab.execute_script("return window.location.href")
        
        current_url = current_url_coroutine['result']['result']['value']
        if current_url == current_main:

            # Enables listening for page events, such as JavaScript dialog events. Without this, dialog events won’t trigger your handler.
            await tab.enable_page_events()

            # 'Page.javascriptDialogOpening' is the name of the event that the Chrome DevTools Protocol emits whenever an alert, confirm, or prompt dialog is about to show.
            

            # Browser → (Sends "event package") → pydoll → (Calls lambda (the callback function) and gives it the "event package") → lambda → (Calls dialog_handler and gives it the "event package") → dialog_handler (Now has the "event package" to work with!).
            await tab.on("Page.javascriptDialogOpening", lambda event: asyncio.create_task(dialog_handler(tab, event))) # .on() expects an event_package and callback function
            # If your callback_function is an async def function, or if it's a lambda that returns a coroutine object (like lambda event: some_async_func(event)),
            # then pydoll will intelligently create an asyncio.Task for it and run it concurrently.

            # When pydoll calls your lambda event: asyncio.create_task(dialog_handler(tab, event)), the lambda receives the event data.

            # Inside the lambda, it immediately calls asyncio.create_task(dialog_handler(tab, event)).

            # asyncio.create_task() takes the dialog_handler coroutine and directly adds it to the asyncio event loop as a concurrent task.

            # The lambda itself returns the Task object (or technically, None if the task is merely scheduled and not awaited), but the crucial part is that the dialog_handler coroutine has already been scheduled.

            # pydoll's events_manager receives the result of the lambda (the task object) and doesn't need to do anything further with it itself, because the task is already running. This satisfies the "awaited" requirement.
            # Then, it registers this Task with the currently running event loop..

            # this line triggers an alert
            await (await tab.find_or_wait_element(By.XPATH, "//button[text()='Click for JS Alert']", find_all=False, raise_exc=True, timeout=5)).click()
            await asyncio.sleep(5)
        
        await tab.close()

if __name__ == "__main__":
    asyncio.run(tag_name_elements())