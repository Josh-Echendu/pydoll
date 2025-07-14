import asyncio
from pydoll.browser import Chrome
from pydoll.constants import By

async def retrieve_attribute_type(locator):
    async with Chrome() as browser:
        tab = await browser.start()
        await tab.go_to("http://omayo.blogspot.com/")
        await asyncio.sleep(3)

        button = await tab.find_or_wait_element(By.ID, locator, find_all=False, raise_exc=True)
        button_type = button.get_attribute("type")
        print(button_type)
        await tab.close()


async def retrieve_attribute_value(locator):
    async with Chrome() as browser:
        tab = await browser.start()
        await tab.go_to("http://omayo.blogspot.com/")
        await asyncio.sleep(3)

        button = await tab.find_or_wait_element(By.XPATH, locator, find_all=False, raise_exc=True)
        print(button)
        button_value = button.get_attribute("value")
        print(button_value)

        await tab.close()

async def main():
    type = asyncio.create_task(retrieve_attribute_type('but2'))
    value = asyncio.create_task(retrieve_attribute_value("//td[@class='gsc-search-button']/input[@title='search']"))

    await asyncio.gather(type, value)

if __name__ == "__main__":
    asyncio.run(main())

