"""
Pydantic models used by the POLARIS-IR API.

These models define the structure of requests and responses for the API
endpoints, making use of type annotations for validation and documentation.
"""

from typing import List, Optional, Dict

from pydantic import BaseModel


class EventItem(BaseModel):
    """Representation of a single event item."""

    id: str
    date: str
    source: str
    title: str
    url: str
    country: Optional[str] = None
    actors: Optional[List[str]] = None
    location: Optional[str] = None
    sentiment: Optional[float] = None
    summary: Optional[str] = None  # additional field for summarised event


class BriefRequest(BaseModel):
    """Request schema for generating a brief."""

    items: List[EventItem]
    focus: Optional[str] = None
    length: Optional[str] = "short"


class BriefSection(BaseModel):
    """Structure of a generated brief section."""

    title: str
    tl_dr: str
    what_happened: str
    why_it_matters: str
    risk_level: str
    indicators: List[str]
    sources: List[str]


class BriefResponse(BaseModel):
    """Wrapper for the brief response."""

    brief: BriefSection


class ScenarioRequest(BaseModel):
    """Request schema for generating scenarios."""

    prompt: str
    actors: List[str]
    time_horizon_days: int
    assumptions: Optional[List[str]] = None
    variants: int = 3


class ScenarioVariant(BaseModel):
    """Representation of a single scenario variant."""

    name: str
    likelihood: float
    narrative: str
    triggers: List[str]
    leading_indicators: List[str]
    policy_options: List[str]


class ScenarioResponse(BaseModel):
    """Wrapper for the scenario response."""

    scenarios: List[ScenarioVariant]


class RiskRequest(BaseModel):
    """Request schema for a risk score calculation."""

    area: str
    window_days: int = 14


class RiskScore(BaseModel):
    """Structure of a risk score response."""

    score: float
    components: Dict[str, float]
    notes: Optional[str] = None
