from contextlib import asynccontextmanager
from playwright.async_api import async_playwright, Browser, Page, BrowserContext
from typing import Optional


class BrowserManager:
    _instance: Optional["BrowserManager"] = None
    _playwright = None
    _browser: Optional[Browser] = None
    _page: Optional[Page] = None
    _context: Optional[BrowserContext] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @asynccontextmanager
    async def get_page_context(self):
        try:
            if self._page is None:
                await self._init_browser()
            yield self._page, self._context
        except Exception as e:
            if self._page:
                await self._page.close()
                self._page = None
            if self._context:
                await self._context.close()
                self._context = None
            raise

    async def _init_browser(self):
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(
            headless=False, args=["--disable-blink-features=AutomationControlled"]
        )
        self._context = await self._browser.new_context()
        self._page = await self._context.new_page()

    async def cleanup(self):
        if self._page:
            await self._page.close()
            self._page = None
        if self._context:
            await self._context.close()
            self._context = None
        if self._browser:
            await self._browser.close()
            self._browser = None
        if self._playwright:
            await self._playwright.stop()
            self._playwright = None
