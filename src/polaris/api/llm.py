"""
API endpoint for interacting with the LLM service.
"""

from fastapi import APIRouter
from pydantic import BaseModel

from polaris.services import llm_service

router = APIRouter(prefix="/v1/llm", tags=["LLM"])


class LLMRequest(BaseModel):
    prompt: str
    sources: list[str] = []
    model: str = "llama3"


@router.post("/generate")
def generate(request: LLMRequest) -> dict:
    """
    Generate a response from the language model.
    """
    response = llm_service.generate_response(prompt=request.prompt, model=request.model, sources=request.sources)
    return {"prompt": request.prompt, "response": response}
