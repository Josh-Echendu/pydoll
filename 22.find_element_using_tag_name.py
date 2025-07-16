import asyncio
from pydoll.browser import Chrome
from pydoll.browser.options import ChromiumOptions
from pydoll.constants import By


async def tag_name_elements():
    options = ChromiumOptions()
    options.add_argument("--start-maximized--")

    async with Chrome() as browser:
        tab = await browser.start()
        await tab.go_to("http://omayo.blogspot.com/")
        await asyncio.sleep(5)
        text_area_1 = await tab.find_or_wait_element(By.XPATH, "(//textarea)[1]", find_all=False, raise_exc=True)
        await text_area_1.type_text("i am a guy")
     
        await asyncio.sleep(5)
        text_areas = await tab.find_or_wait_element(By.TAG_NAME, 'textarea', find_all=True, raise_exc=True)

        for text_area in text_areas:
            print(await text_area.text)

        all_links = await tab.find_or_wait_element(By.TAG_NAME, "a", find_all=True, raise_exc=True)
        for i, link in enumerate(all_links):
            print(f"Link {i}: {link.get_attribute('href')}")

        await tab.close()

if __name__ == "__main__":
    asyncio.run(tag_name_elements())