from fastapi import APIRouter, HTTPException
from app.models.schemas import UserRequest, AIWorkflowRecipe
from app.services.matcher_service import StackOptimizerService

router = APIRouter()
optimizer_service = StackOptimizerService()

@router.post("/optimize", response_model=AIWorkflowRecipe, summary="Generate AI Stack Recipe")
async def get_ai_recommendation(request: UserRequest):
    try:
        recipe = optimizer_service.generate_recipe(request)
        return recipe
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))