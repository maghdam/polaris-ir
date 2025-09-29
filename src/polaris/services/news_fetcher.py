"""
Service for fetching news events.

This module provides an implementation for fetching events from the GDELT DOC API.
"""

from typing import List
import gdeltdoc
from polaris.models import EventItem
import datetime

def fetch_events(q: str = "", countries: str = "", since: str = "", until: str = "", maxrecs: int = 50) -> List[EventItem]:
    """Return a list of events from GDELT DOC API.

    Parameters
    ----------
    q: str
        Query string or keywords to search for.
    countries: str
        Comma-separated list of ISO country codes.
    since: str
        Start date (ISO 8601).
    until: str
        End date (ISO 8601).
    maxrecs: int
        Maximum number of records to return.

    Returns
    -------
    List[EventItem]
        A list of EventItem objects from GDELT.
    """

    if not since:
        since = (datetime.datetime.utcnow() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    if not until:
        until = datetime.datetime.utcnow().strftime("%Y-%m-%d")

    filters = gdeltdoc.Filters(
        start_date=since,
        end_date=until,
        keyword=q,
        country=countries.split(",") if countries else None,
        num_records=maxrecs
    )

    gd = gdeltdoc.GdeltDoc()

    articles = gd.article_search(filters)

    events: List[EventItem] = []
    if articles is not None and not articles.empty:
        for index, row in articles.iterrows():
            events.append(
                EventItem(
                    id=row["url"],  # GDELT DOC API does not provide a stable ID
                    date=row["seendate"],
                    source=row["domain"], 
                    title=row["title"],
                    url=row["url"],
                    country=row["sourcecountry"],
                    actors=[], # Not directly available in DOC API
                    location=None, # Not directly available in DOC API
                    sentiment=float(row["tone"]) if "tone" in row else None,
                    summary=None # Not directly available in DOC API
                )
            )
            
    return events
