"""
Service for performing data analysis on dataframes.
"""

import pandas as pd

def get_total_fatalities(df: pd.DataFrame, country: str, year: int) -> int:
    """Get the total number of fatalities for a given country and year."""
    return df[(df['country'] == country) & (df['year'] == year)]['best'].sum()
