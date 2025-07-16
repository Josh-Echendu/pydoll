import asyncio
from pydoll.browser import Chrome
from pydoll.constants import By
from pydoll.browser.options import ChromiumOptions




async def check_button_enabled():
    options = ChromiumOptions()

    options.add_argument('--start-maximized')
    
    async with Chrome(options=options) as browser:
        tab = await browser.start()
        await tab.go_to("http://omayo.blogspot.com/")
        await asyncio.sleep(3)

        radio_button = await tab.find_or_wait_element(By.XPATH, "//input[@value='Bicycle']", raise_exc=True, find_all=False)
        print(radio_button)

        #<input type="radio" checked> <!-- unchecked -->
        #<input type="radio" checked=""> <!-- checked -->
        #<input type="radio" checked="true"> <!-- checked -->

        checked_atribute = radio_button.get_attribute('checked')

        # note empty string (" ") means its a string, it is not the same as None, there is a value in it
        if checked_atribute is not None:
            print("selected")
        else:
            print("not selected")

        checked_atr = await tab.execute_script("""
            const select = arguments[0];
            select.hasAttribute('checked')
        """, radio_button)

        if checked_atr:
            print("selected")
        else:
            print("not selected")

        await asyncio.sleep(5)
        await tab.close()


if __name__ == "__main__":
    asyncio.run(check_button_enabled())
