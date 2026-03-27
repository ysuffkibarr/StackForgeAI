from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class UserRequest(BaseModel):
    task_description: str = Field(..., example="Write a Python script to scrape data from a website.")
    budget_priority: str = Field(default="balanced", example="Options: 'cheap', 'balanced', 'premium'")
    speed_priority: str = Field(default="balanced", example="Options: 'fast', 'balanced', 'quality'")
    requires_vision: bool = Field(default=False, description="Does the task require vision capabilities?")

class PerformanceMetrics(BaseModel):
    coding: float
    creative_writing: float
    logic_reasoning: float
    speed: float
    image_quality: Optional[float] = None

class AIModelInfo(BaseModel):
    model_id: str
    name: str
    provider: str
    modality: str
    performance_metrics: PerformanceMetrics
    use_cases: List[str]

class RecommendedStep(BaseModel):
    step_number: int
    action_type: str = Field(..., example="Coding")
    recommended_model: str = Field(..., example="Claude 3.5 Sonnet")
    reason: str = Field(..., example="This model excels in coding tasks and has a good balance of speed and quality.")
    estimated_cost_level: str = Field(None, example="High ($15/1M token)")

class AIWorkflowRecipe(BaseModel):
    original_task: str
    overral_strategy: str = Field(..., example="Balanced approach prioritizing quality while keeping costs reasonable.")
    steps: List[RecommendedStep]
    alternative_budget_options: Optional[str] = Field(None, example="If you have a tight budget, you can use Llama 3 (70B) to leave.")