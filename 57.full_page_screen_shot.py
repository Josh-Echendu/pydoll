import asyncio
import base64
import os
import aiofiles

from pydoll.browser import Chrome
from pydoll.commands.runtime_commands import RuntimeCommands
from pydoll.commands.page_commands import PageCommands

async def main():
    async with Chrome() as browser:
        tab = await browser.start()

        await tab.go_to("https://1xbet.whoscored.com/")
        await asyncio.sleep(5)

        #➡ This runs JavaScript inside the page to find the true width and height of everything scrollable.
        js_dimensions = RuntimeCommands.evaluate(
            expression="""
            ({
                width: Math.max(
                    document.documentElement.scrollWidth,
                    document.body.scrollWidth
                ),
                height: Math.max(
                    document.documentElement.scrollHeight,
                    document.body.scrollHeight
                )
            })
            """,
            return_by_value=True
        )
        result = await tab._connection_handler.execute_command(js_dimensions)
        print(result)
        width = result['result']['result']['value']['width']
        await asyncio.sleep(3)
        height = result['result']['result']['value']['height']
        print(f"[+] Detected page size: width={width}, height={height}")

        # Step 2: Manually dispatch Emulation.setDeviceMetricsOverride
        metrics_command = { # ➡ This tells Chrome to resize the visible area of the page to match the full size of the content.
            "method": "Emulation.setDeviceMetricsOverride",
            "params": {
                "width": width,
                "height": height,
                "deviceScaleFactor": 1,
                "mobile": False
            }
        }
        await tab._connection_handler.execute_command(metrics_command)

        # Step 3: Full screenshot (no clip = full viewport)
        capture_cmd = PageCommands.capture_screenshot(format="png", quality=100)
        screenshot_result = await tab._connection_handler.execute_command(capture_cmd)

        image_data = base64.b64decode(screenshot_result['result']['data'])
        base_dir = r"/Users/joshua.echendu/Documents/pydoll/pydoll/screenshot"
        path = os.path.join(base_dir, "full_page.png")

        async with aiofiles.open(path, 'wb') as file:
            await file.write(image_data)

        print(f"[✓] Screenshot saved at: {path}")

        await tab.close()

if __name__ == "__main__":
    asyncio.run(main())
