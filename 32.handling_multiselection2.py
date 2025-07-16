import asyncio
from pydoll.browser import Chrome
from pydoll.constants import By
from pydoll.browser.options import ChromiumOptions

async def handle_multiselection():
    options = ChromiumOptions()
    options.add_argument('--start-maximized')

    async with Chrome(options=options) as browser:
        tab = await browser.start()
        await tab.go_to("http://omayo.blogspot.com/")
        await asyncio.sleep(3)

        # Locate the <select> element
        select_element = await tab.find_or_wait_element(By.ID, "multiselect1")

        # Determine if the <select> is a multiselection box
        is_multiple = await tab.execute_script("""
            const select = argument[0];
            return select.hasAttribute('multiple');
        """, select_element)

        if not is_multiple:
            print("Drop down box")

        else:
            print("Multiselection box")

        selected_texts = await tab.execute_script("""
            const select = document.getElementById('multiselect1');
            const selected = [];
            for (let i = 0; i < select.options.length; i++) {
                if (select.options[i].selected) {
                    selected.push(select.options[i].text);
                }
            }
            return selected;
        """)
        print("Selected options:", selected_texts)


        await asyncio.sleep(3)

if __name__ == "__main__":
    asyncio.run(handle_multiselection())
