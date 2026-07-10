from pydantic import BaseModel
from typing import List

class AgentRequest(BaseModel):
    request: str

class AgentResponse(BaseModel):
    status: str
    request_understood_as: str
    tasks_completed: List[str]
    document_type: str
    reflection_iterations: int
    file_path: str

