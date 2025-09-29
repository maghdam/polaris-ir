"""
Router for the /generate-brief endpoint.

This endpoint accepts a list of event items and optional parameters and returns
a structured brief summarising what happened, why it matters, and risks.
"""

import json
from fastapi import APIRouter

from polaris.models import BriefRequest, BriefResponse, BriefSection
from polaris.prompts import create_brief_prompt
from polaris.services.llm_service import generate_response


router = APIRouter(prefix="/generate-brief", tags=["brief"])


@router.post("", response_model=BriefResponse)
def generate_brief(request: BriefRequest) -> BriefResponse:
    """Generate a simple brief from the provided events.
    
    This endpoint uses an LLM to generate a structured brief based on the
    provided event items.
    """
    prompt = create_brief_prompt(request.items, request.focus)
    llm_response_str = generate_response(prompt)
    sources = [item.url for item in request.items]

    try:
        # The LLM is instructed to return JSON, so we parse it.
        brief_data = json.loads(llm_response_str)
        brief_section = BriefSection(
            title=f"Brief on {request.focus or 'selected events'}",
            tl_dr=brief_data.get("tl_dr", "Summary not available."),
            what_happened=brief_data.get("what_happened", "Narrative not available."),
            why_it_matters=brief_data.get("why_it_matters", "Impact analysis not available."),
            risk_level=brief_data.get("risk_level", "Unknown"),
            indicators=brief_data.get("indicators", []),
            sources=sources,
        )
    except (json.JSONDecodeError, TypeError):
        # Fallback if the LLM response is not valid JSON
        brief_section = BriefSection(
            title=f"Brief on {request.focus or 'selected events'}",
            tl_dr="Could not generate a structured summary.",
            what_happened=llm_response_str, # Return the raw text
            why_it_matters="Analysis could not be performed.",
            risk_level="Unknown",
            indicators=[],
            sources=sources,
        )
    return BriefResponse(brief=brief_section)
