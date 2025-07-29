from pydoll.browser import Chrome
from pydoll.commands.page_commands import PageCommands
from pydoll.commands.runtime_commands import RuntimeCommands
import asyncio

async def main():
    async with Chrome() as browser:
        tab = await browser.start()

        # Bypass page's Content Security Policy
        await tab._connection_handler.execute_command(
            PageCommands.set_bypass_csp(enabled=True)
        )

        await tab.go_to("https://example.com")
        await asyncio.sleep(2)

        # Inject a simple alert (would normally be blocked on some CSP pages)
        js = RuntimeCommands.evaluate(expression="alert('Bypassed CSP!')")
        await tab._connection_handler.execute_command(js)

        await asyncio.sleep(3)
        await tab.close()

if __name__ == "__main__":
    asyncio.run(main())
