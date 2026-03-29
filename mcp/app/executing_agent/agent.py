import uuid
from ollama import chat

from app.executing_agent.client import MCPClient


class Agent:
    def __init__(self, server_module: str, model_name: str, system_prompt_file: str):
        self.client = MCPClient(server_module)
        self.model_name = model_name
        self.system_prompt_file = system_prompt_file
        self.tools = []
        self.messages = []

    async def __aenter__(self):
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.cleanup()

    async def initialize(self) -> list:
        print(f"{'=' * 50}\n🧪 initializing agent")
        try:
            mcp_tools = await self.client.connect()
            self.tools = self._convert_to_ollama_tools(mcp_tools)
            with open(self.system_prompt_file, "r", encoding="utf-8") as f:
                system_prompt = f.read()
            self.messages.append({"role": "system", "content": system_prompt})
            print(f"📗 agent initialized successfully: {len(self.tools)} tools")
        except Exception as e:
            print(f"📕 initialize error: {e}")
            await self.client.cleanup()
            raise

    @staticmethod
    def _convert_to_ollama_tools(mcp_tools):
        ollama_tools = []
        for t in mcp_tools:
            ollama_tools.append({
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description,
                    "parameters": t.inputSchema
                }
            })
        return ollama_tools

    async def run(self, user_prompt: str, max_steps: int) -> list[dict]:
        self.messages.append({"role": "user", "content": user_prompt})
        print(f"{'=' * 50}\n📋 user prompt:\n{user_prompt}")

        await self.client.call_tool("navigate", {"url": "about:blank"})

        for _ in range(max_steps):
            response = chat(
                model=self.model_name,
                messages=self.messages,
                tools=self.tools,
                options={"temperature": 0.1}
            )
            message = response["message"]
            self.messages.append(message)

            if not message.get("tool_calls"):
                return {"output": message["content"], "messages": self.messages}

            for tool_call in message["tool_calls"]:
                tool_name = tool_call["function"]["name"]
                tool_args = tool_call["function"]["arguments"]
                print(f"{'=' * 50}\n🔧 tool:\n{tool_name}, args: {tool_args}")
                result = await self.client.call_tool(tool_name, tool_args)
                print(f"{'=' * 50}\n🕹️  result:\n{str(result)[:300] if result else '(empty)'}")
                self.messages.append({
                    "role": "tool",
                    "content": result if result else "",
                    "tool_call_id": str(uuid.uuid4())
                })
        return {"output": "max steps reached", "messages": self.messages}
