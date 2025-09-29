"""
Core configuration for the POLARIS-IR application.

This module defines the data models for data sources and manages the loading
and saving of data source configurations.
"""

import json
from pydantic import BaseModel, Field
from typing import List, Literal

class DataSource(BaseModel):
    """Represents a single data source for the RAG system."""
    name: str = Field(..., description="The human-readable name of the data source.")
    type: Literal["csv", "api", "website"] = Field(..., description="The type of the data source.")
    url: str = Field(..., description="The URL or endpoint of the data source.")
    codebook_url: str = Field(None, description="The URL of the codebook for the data source.")

def get_default_data_sources() -> List[DataSource]:
    """Return a list of default data sources."""
    return []

def load_data_sources() -> List[DataSource]:
    """Load data sources from a JSON file, or create it if it doesn't exist."""
    try:
        with open("data_sources.json", "r") as f:
            data = json.load(f)
            return [DataSource(**item) for item in data]
    except (FileNotFoundError, json.JSONDecodeError):
        save_data_sources([]) # Create an empty file
        return []

def save_data_sources(data_sources: List[DataSource]):
    """Save data sources to a JSON file."""
    with open("data_sources.json", "w") as f:
        json.dump([source.dict() for source in data_sources], f, indent=4)
