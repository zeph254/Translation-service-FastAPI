from pydantic import BaseModel
from typing import Dict,List

class TranslationRequest(BaseModel):  # ✅ Fixed class name capitalization
    text: str
    languages: List[str]  # ✅ Ensure consistency (not "language")

class TaskResponse(BaseModel):
    task_id: int

class TranslationStatus(BaseModel):
    task_id: int
    status: str
    translations: Dict[str, str]
