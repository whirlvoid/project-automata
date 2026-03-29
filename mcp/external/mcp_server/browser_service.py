import asyncio

from external.mcp_server.browser_manager import BrowserManager
from external.mcp_server.page_parser import PageParser


class BrowserService:
    def __init__(self):
        self.manager = BrowserManager()
        self.parser = PageParser()
        self.screenshot_history = []

    async def navigate(self, url: str):
        async with self.manager.get_page_context() as (p, c):
            try:
                await p.goto(url)
                await c.pages[0].bring_to_front()
                await p.wait_for_load_state("domcontentloaded")
                page_url = p.url
                return f"OK: navigated to {page_url}"
            except Exception as e:
                return f"ERROR: {e}"

    async def click(self, selector: str):
        async with self.manager.get_page_context() as (p, _):
            try:
                await p.wait_for_selector(selector)
                await p.click(selector)
                return f"OK: clicked {selector}"
            except Exception as e:
                return f"ERROR: {e}"

    async def get_text(self, selector: str):
        async with self.manager.get_page_context() as (p, _):
            try:
                await p.wait_for_selector(selector)
                text = await p.text_content(selector)
                return f"OK: {text.strip() if text else ''}"
            except Exception as e:
                return f"ERROR: {e}"

    async def type_text(self, selector: str, text: str):
        async with self.manager.get_page_context() as (p, _):
            try:
                await p.wait_for_selector(selector)
                await p.fill(selector, text)
                return f"OK: typed into {selector}"
            except Exception as e:
                return f"ERROR: {e}"

    async def get_interactive_elements(self):
        async with self.manager.get_page_context() as (p, _):
            try:
                html = await p.content()
                parsed = self.parser.interactive_parse(html)
                return f"OK:\n{parsed}"
            except Exception as e:
                return f"ERROR: {e}"

    async def get_text_elements(self):
        async with self.manager.get_page_context() as (p, _):
            try:
                html = await p.content()
                parsed = self.parser.texts_parse(html)
                return f"OK:\n{parsed}"
            except Exception as e:
                return f"ERROR: {e}"

    async def get_current_state(self):
        async with self.manager.get_page_context() as (p, _):
            try:
                title = await p.title()
                url = p.url

                return f"OK: URL={url} TITLE={title} TITLE={title} TIMESTAMP={asyncio.get_event_loop().time()}"
            except Exception as e:
                return f"ERROR: {e}"
