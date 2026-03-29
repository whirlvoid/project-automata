from pathlib import Path

BASE_DIR = Path(__file__).parent
SYSTEM_PROMPT_PATH = BASE_DIR / "executing_agent" / "system_prompt.txt"
MCP_SERVER_MODULE = "external.mcp_server.main"

MODELS = ["qwen3:0.6b"]

MAX_STEPS_DEFAULT = 5
MAX_STEPS_GE = 0
MAX_STEPS_LE = 20
