"""
Router for the /generate-scenario endpoint.

This endpoint accepts a scenario request and returns multiple scenario variants.
"""

from fastapi import APIRouter

from polaris.models import ScenarioRequest, ScenarioResponse
from polaris.services.scenario_generator import generate_scenarios


router = APIRouter(prefix="/generate-scenario", tags=["scenario"])


@router.post("", response_model=ScenarioResponse)
def generate_scenario(request: ScenarioRequest) -> ScenarioResponse:
    """Generate scenario variants based on the provided input.

    Delegates to the ``scenario_generator.generate_scenarios`` service.  The
    returned scenarios include dummy values for demonstration.
    """
    scenarios = generate_scenarios(
        prompt=request.prompt,
        actors=request.actors,
        horizon=request.time_horizon_days,
        assumptions=request.assumptions or [],
        variants=request.variants,
    )
    return ScenarioResponse(scenarios=scenarios)
