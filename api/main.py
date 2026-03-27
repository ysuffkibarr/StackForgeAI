from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import recommend

app = FastAPI(
    title="StackForge AI API",
    description="The Ultimate AI Stack Optimizer & Workflow Recommender",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recommend.router, prefix="/api/v1", tags=["Recommendation Engine"])

@app.get("/")
async def root():
    return {"message": "Welcome to StackForge AI. Visit /docs for the API documentation."}