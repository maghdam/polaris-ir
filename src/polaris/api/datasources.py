"""
Router for the /datasources endpoint.

This router exposes endpoints for listing and adding data sources.
"""

from typing import List

from fastapi import APIRouter, HTTPException

from polaris.core.config import DataSource, load_data_sources, save_data_sources

router = APIRouter(prefix="/api/datasources", tags=["datasources"])


@router.get("", response_model=List[DataSource])
def list_data_sources() -> List[DataSource]:
    """Return a list of all configured data sources."""
    return load_data_sources()


@router.post("", response_model=DataSource)

def add_data_source(data_source: DataSource) -> DataSource:
    """Add a new data source to the configuration."""
    sources = load_data_sources()
    sources.append(data_source)
    save_data_sources(sources)
    return data_source
