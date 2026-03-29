from fastmcp import FastMCP

from external.mcp_server.browser_service import BrowserService

browser_service = BrowserService()


def register_tools(mcp: FastMCP):

    @mcp.tool()
    async def test_tool() -> str:
        """Return fixed string 'TOOL_USED'."""
        return "TOOL_USED"

    @mcp.tool()
    async def navigate(url: str) -> str:
        """Navigate to a URL"""
        result = await browser_service.navigate(url)
        return result

    @mcp.tool()
    async def click(selector: str) -> str:
        """Click on an element by selector"""
        result = await browser_service.click(selector)
        return result

    @mcp.tool()
    async def get_text(selector: str) -> str:
        """Get the text of an element by selector"""
        result = await browser_service.get_text(selector)
        return result

    @mcp.tool()
    async def type_text(selector: str, text: str) -> str:
        """Type text into an input field"""
        result = await browser_service.type_text(selector, text)
        return result

    @mcp.tool()
    async def get_interactive_elements() -> str:
        """Get information about the structure of the first interactive elements"""
        result = await browser_service.get_interactive_elements()
        return result

    @mcp.tool()
    async def get_text_elements() -> str:
        """Get information about the structure of the first text elements"""
        result = await browser_service.get_text_elements()
        return result

    @mcp.tool()
    async def get_current_state() -> str:
        """Get the current state of the page"""
        result = await browser_service.get_current_state()
        return result

    return mcp
