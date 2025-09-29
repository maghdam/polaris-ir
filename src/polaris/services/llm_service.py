"""
Service for interacting with the LLM.

This service now uses a multi-agent system to generate responses.
"""

from polaris.agents.orchestrator import OrchestratorAgent

orchestrator_agent = OrchestratorAgent()

def generate_response(prompt: str, model: str = "llama3", sources: list[str] = []) -> str:
    """
    Generates a response from the language model.
    """
    return orchestrator_agent.run(prompt, sources=sources, model=model)
