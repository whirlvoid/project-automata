import os
from fastapi import APIRouter, HTTPException
from app.api.execution_model import ExecutionRequest, ExecutionResponse
from app.api.execution_service import ExecutionService

router = APIRouter(prefix="/api/v1.0", tags=["execution"])

project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
execution_service = ExecutionService(project_root)


@router.post("/execute", response_model=ExecutionResponse)
async def execute(req: ExecutionRequest):
    try:
        result = await execution_service.execute(
            model_name=req.model_name,
            user_prompt=req.user_prompt,
            max_steps=req.max_steps,
        )
        return ExecutionResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
