from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPClient:
    def __init__(self, server_module: str):
        self.server_module = server_module
        self.client = None
        self.session = None
        self.tools = []

    async def connect(self):
        params = StdioServerParameters(command="python", args=["-m", self.server_module])
        self.client = stdio_client(params)
        read_stream, write_stream = await self.client.__aenter__()
        self.session = await ClientSession(read_stream, write_stream).__aenter__()
        await self.session.initialize()
        result = await self.session.list_tools()
        self.tools = result.tools
        return self.tools

    async def call_tool(self, name: str, args: dict) -> str:
        result = await self.session.call_tool(name, args)
        return result.content[0].text

    async def cleanup(self):
        if self.session:
            await self.session.__aexit__(None, None, None)
            self.session = None
        if hasattr(self, "client") and self.client:
            await self.client.__aexit__(None, None, None)
            self.client = None
