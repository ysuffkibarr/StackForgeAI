import json
import os
from typing import List, Dict, Any
from app.models.schemas import UserRequest, AIWorkflowRecipe, RecommendedStep

def load_models_db() -> List[Dict[str, Any]]:
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'models_db.json')
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

class StackOptimizerService:
    def __init__(self):
        self.models_db = load_models_db()
        
        self.intent_keywords = {
            "coding": ["code", "app", "website", "software", "bug", "script", "develop", "backend", "frontend"],
            "image_generation": ["image", "logo", "picture", "art", "draw", "design", "photo", "mockup"],
            "creative_writing": ["write", "blog", "article", "story", "essay", "post", "content"]
        }

    def _analyze_intent(self, text: str) -> List[str]:
        """Analyzes the user's prompt to detect required tasks."""
        text_lower = text.lower()
        detected_intents = []
        
        for intent, keywords in self.intent_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                detected_intents.append(intent)

        if not detected_intents:
            detected_intents.append("general_purpose")
            
        return detected_intents

    def _find_best_model(self, intent: str, budget_priority: str) -> Dict[str, Any]:
        """Scores and filters models based on intent and user constraints."""
        best_model = None
        highest_score = -1
        
        for model in self.models_db:
            score = 0

            if intent == "image_generation" and model["modality"] == "text-to-image":
                score += model["performance_metrics"].get("image_quality", 0)
            elif intent == "coding" and model["modality"] == "text-to-text":
                score += model["performance_metrics"].get("coding", 0)
            elif intent == "creative_writing" and model["modality"] == "text-to-text":
                score += model["performance_metrics"].get("creative_writing", 0)
            elif intent == "general_purpose" and model["modality"] == "text-to-text":
                score += model["performance_metrics"].get("logic_reasoning", 0)
            
            if score == 0:
                continue
                
            if budget_priority == "cheap":
                if model["pricing"].get("is_free_tier_available", False):
                    score += 5
                elif model["pricing"].get("input_cost_per_1m", 0) < 1.0:
                    score += 3
            
            if score > highest_score:
                highest_score = score
                best_model = model
                
        return best_model

    def generate_recipe(self, request: UserRequest) -> AIWorkflowRecipe:
        """The main pipeline that constructs the final AI Stack Recipe."""
        intents = self._analyze_intent(request.task_description)
        steps = []
        step_counter = 1
        
        for intent in intents:
            best_match = self._find_best_model(intent, request.budget_priority)
            
            if best_match:
                cost_level = "Free/Cheap" if best_match["pricing"].get("is_free_tier_available") else "Premium"
                
                step = RecommendedStep(
                    step_number=step_counter,
                    action_type=intent.replace("_", " ").title(),
                    recommended_model=best_match["name"],
                    reason=f"Scored highest for {intent} considering your '{request.budget_priority}' budget priority.",
                    estimated_cost_level=cost_level
                )
                steps.append(step)
                step_counter += 1

        overall_strategy = "Sequential Workflow: Complete text/code generation first, followed by visual assets if required."
        
        return AIWorkflowRecipe(
            original_task=request.task_description,
            overall_strategy=overall_strategy,
            steps=steps,
            alternative_budget_option="Check Llama 3 for text tasks if you need a completely free open-source alternative." if request.budget_priority != "cheap" else None
        )