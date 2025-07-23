from pydoll.browser import Chrome
from pydoll.constants import By
from pydoll.browser.options import ChromiumOptions
import asyncio

async def checkbox_radio_button():
    async with Chrome() as browser:
        tab = await browser.start()

        await tab.go_to("https://docs.oracle.com/javase/8/docs/api/")

        await asyncio.sleep(3)

        iframe_element = await tab.find_or_wait_element(By.NAME, "classFrame", timeout=10)
        print("iframe_element: ", iframe_element)
        print('tag_name: ', iframe_element.tag_name)
        print("Name: ", iframe_element.get_attribute("name"))
        print("SRC: ", iframe_element.get_attribute("src"))
        innerhtml = await iframe_element.inner_html
        print("Inner HTML: ", innerhtml)

        # Extract iframe source URL
        frame_src = iframe_element.get_attribute("src")

        # Get the base URL
        base_url = "https://docs.oracle.com/javase/8/docs/api/"

        # Construct the full URL for the iframe
        frame_url = f"{base_url}{frame_src}"

        # Navigation directly to the iframe source URL
        await tab.go_to(frame_url)
        print("Navigated to iframe URL:", frame_url)

        await asyncio.sleep(3)

        description_link = await tab.find(text="Description", tag_name="a")

        await description_link.click()

        print("description: text: ", await description_link.text)

        await asyncio.sleep(30)

        await tab.close()

if __name__ == "__main__":
    asyncio.run(checkbox_radio_button())
