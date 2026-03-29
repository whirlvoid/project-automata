from app.executing_agent.agent import Agent
from app.config import MCP_SERVER_MODULE, SYSTEM_PROMPT_PATH


class ExecutionService:
    def __init__(self, project_root: str):
        self.project_root = project_root

    async def execute(self, model_name: str, user_prompt: str, max_steps: int):
        async with Agent(MCP_SERVER_MODULE, model_name, str(SYSTEM_PROMPT_PATH)) as agent:
            result = await agent.run(user_prompt, max_steps)
            return result
