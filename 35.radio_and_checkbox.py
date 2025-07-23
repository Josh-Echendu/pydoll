from pydoll.browser import Chrome
from pydoll.constants import By
from pydoll.browser.options import ChromiumOptions
import asyncio

async def checkbox_radio_button():
    async with Chrome() as browser:
        tab = await browser.start()

        await tab.go_to("http://omayo.blogspot.com/")

        await asyncio.sleep(3)

        radio_button = await tab.find_or_wait_element(By.ID, "radio1")

        is_radio_checked = await tab.execute_script("""
            const radio1 = argument;
            radio1.hasAttribute("checked");
        """, radio_button)
        print(f"Is radio button checked: {is_radio_checked}")   

        if is_radio_checked:
            print("Radio button is checked")
        else:
            await radio_button.click()

        checkbox = await tab.find_or_wait_element(By.ID, "checkbox1")
        
        is_checkbox_checked = await tab.execute_script("""
            const checkbox = argument[0];
            checkbox.hasAttribute("checked");
        """, checkbox)

        if is_checkbox_checked:
            print("checkbox is checked")
        else:
            checkbox.click()


        await asyncio.sleep(30)

        await tab.close()

if __name__ == "__main__":
    asyncio.run(checkbox_radio_button())
