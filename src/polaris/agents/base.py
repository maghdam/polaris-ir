"""
Base class for all agents.
"""

from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """Abstract base class for all agents."""

    @abstractmethod
    def run(self, prompt: str, **kwargs) -> str:
        """Run the agent."""
        pass
