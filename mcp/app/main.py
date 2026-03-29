import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.execution_controller import router as execution_router

app = FastAPI(title="browser_agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(execution_router)


@app.get("/ok")
async def ok_ckech():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
