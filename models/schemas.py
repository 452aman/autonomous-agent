from pydantic import BaseModel, field_validator
from typing import List, Optional
from datetime import datetime


class AgentRequest(BaseModel):
    request: str

    @field_validator("request")
    @classmethod
    def validate_request(cls, v):
        v = v.strip()
        if len(v) < 10:
            raise ValueError("Request is too short. Please provide more detail (min 10 characters).")
        if len(v) > 1000:
            raise ValueError("Request is too long. Please keep it under 1000 characters.")
        if v.replace(" ", "").isdigit():
            raise ValueError("Request must be a meaningful sentence, not just numbers.")
        return v


class AgentResponse(BaseModel):
    status: str
    document_type: str
    tasks_completed: List[str]
    reflection_iterations: int
    file_path: str


class HistoryEntry(BaseModel):
    id: int
    request: str
    document_type: str
    tasks_completed: List[str]
    reflection_iterations: int
    file_path: str
    timestamp: str
