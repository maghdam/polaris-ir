"""
This module contains prompt templates for interacting with the LLM.
"""

from typing import List
from polaris.models import EventItem


def create_brief_prompt(items: List[EventItem], focus: str = None) -> str:
    """
    Creates a prompt for the LLM to generate a structured brief from a list of events.

    Args:
        items: A list of EventItem objects.
        focus: The specific focus for the brief.

    Returns:
        A formatted prompt string.
    """
    event_list = "\n".join(
        [f"- {item.date}: {item.title} (Source: {item.source})" for item in items]
    )

    focus_instruction = (
        f"The specific focus for this brief is: {focus}." if focus else ""
    )

    return f"""You are POLARIS-IR Assistant, an AI for international security analysis.
Your task is to generate a structured intelligence brief based on the following events.

Events:
{event_list}

{focus_instruction}

Generate a brief with the following sections:
- TL;DR: A one-sentence summary.
- What Happened: A concise narrative of the events.
- Why It Matters: The geopolitical or security impact.
- Risk Level: Assess the risk as Low, Medium, or High.
- Leading Indicators: 2-3 indicators to watch for future developments.

Format your response as a JSON object with keys: "tl_dr", "what_happened", "why_it_matters", "risk_level", "indicators".
"""