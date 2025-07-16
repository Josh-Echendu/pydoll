import asyncio
from pydoll.browser import Chrome
from pydoll.constants import By
from pydoll.browser.options import ChromiumOptions

async def main():
    options = ChromiumOptions()
    options.add_argument('--start-maximized')
    options.add_argument("--window-size=1920,1080")

    async with Chrome(options=options) as browser:
        tab = await browser.start()
        await tab.go_to("https://tutorialsninja.com/demo/")
        await asyncio.sleep(3)

        # Find the search input by name
        search_input = await tab.find_or_wait_element(By.NAME, "search")
        await tab.
        # Use JS to get bounding box
        script = """
            const rect = argument.getBoundingClientRect();
            return {
                x: rect.x,
                y: rect.y,
                width: rect.width,
                height: rect.height
            };
        """
        result = await tab.execute_script(script, search_input)
        bounding_box = result["result"]["result"]["value"]
        print(bounding_box)
        print(bounding_box.get("width"))
        print(bounding_box.get("height"))
        print(bounding_box.get("x"))
        print(bounding_box.get("y"))

        await tab.close()

if __name__ == "__main__":
    asyncio.run(main())