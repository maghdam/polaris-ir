"""
Service for generating scenario narratives.

This module provides a simple stub that returns a list of scenario variants
based on the input prompt.  In a real system you might integrate a
language model or simulation engine here.
"""

from typing import List
import random

from polaris.models import ScenarioVariant


def generate_scenarios(prompt: str, actors: List[str], horizon: int, assumptions: List[str], variants: int) -> List[ScenarioVariant]:
    """Generate scenario variants based on a prompt and parameters.

    This stub returns a list of variants with dummy values.  Replace with
    logic that uses LLMs, simulation or expert rules for meaningful
    scenarios.

    Parameters
    ----------
    prompt: str
        Description of the scenario (e.g. a potential future event).
    actors: List[str]
        Key actors involved in the scenario.
    horizon: int
        Time horizon in days for the scenario.
    assumptions: List[str]
        List of assumptions to consider.
    variants: int
        Number of variants to generate.
    """

    scenario_list: List[ScenarioVariant] = []
    for i in range(variants):
        scenario_list.append(
            ScenarioVariant(
                name=f"Variant {i + 1}",
                likelihood=round(random.uniform(0.2, 0.8), 2),
                narrative=f"{prompt} scenario narrative {i + 1}. Actors involved: {', '.join(actors)}.",
                triggers=[f"Trigger {j}" for j in range(1, 4)],
                leading_indicators=[f"Indicator {j}" for j in range(1, 4)],
                policy_options=[f"Policy option {j}" for j in range(1, 4)],
            )
        )
    return scenario_list
