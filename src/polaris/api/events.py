"""
Router for the /fetch-events endpoint.

This router exposes a GET endpoint for retrieving a list of events.  It
delegates the actual fetching to the ``news_fetcher`` service.  Clients can
specify query parameters to filter events by keywords, countries and
date ranges.
"""

from typing import List

from fastapi import APIRouter, Query

from polaris.models import EventItem
from polaris.services.news_fetcher import fetch_events


router = APIRouter(prefix="/fetch-events", tags=["events"])


@router.get("", response_model=List[EventItem])
def fetch_events_endpoint(
    q: str = Query("", description="Query string for event search"),
    countries: str = Query("", description="Comma-separated country codes"),
    since: str = Query("", description="Start date (YYYY-MM-DD)"),
    until: str = Query("", description="End date (YYYY-MM-DD)"),
    max: int = Query(50, description="Maximum number of events to return"),
) -> List[EventItem]:
    """Return a list of events.

    This endpoint proxies the request to the ``news_fetcher.fetch_events`` service.
    The response is a list of ``EventItem`` objects.
    """
    events = fetch_events(q=q, countries=countries, since=since, until=until, maxrecs=max)
    return events
