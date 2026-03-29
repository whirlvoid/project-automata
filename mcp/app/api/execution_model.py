from pydantic import BaseModel, Field
from typing import Literal

from app.config import MAX_STEPS_DEFAULT, MAX_STEPS_GE, MAX_STEPS_LE, MODELS


class ExecutionRequest(BaseModel):
    model_name: Literal[(tuple(MODELS))] = MODELS[0]
    user_prompt: str
    max_steps: int = Field(default=MAX_STEPS_DEFAULT, ge=MAX_STEPS_GE, le=MAX_STEPS_LE)


class ExecutionResponse(BaseModel):
    output: str
    messages: list
