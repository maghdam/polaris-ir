"""
Service for loading data from various sources.

This module provides functions to load data from different types of sources,
including CSV files from URLs, APIs, and websites.
"""

import pandas as pd
import requests
import zipfile
import io
from pypdf import PdfReader

def load_csv(location: str) -> pd.DataFrame:
    """Load a CSV file from a URL or a local file path, handling zip files."""
    if location.startswith('http'):
        response = requests.get(location)
        response.raise_for_status()  # Raise an exception for bad status codes
        content = response.content
    else:
        with open(location, 'rb') as f:
            content = f.read()

    if location.endswith('.zip'):
        with zipfile.ZipFile(io.BytesIO(content)) as z:
            # Find the first CSV file in the zip archive
            csv_file = next((f for f in z.namelist() if f.endswith('.csv')), None)
            if csv_file:
                with z.open(csv_file) as f:
                    return pd.read_csv(f)
            else:
                raise ValueError("No CSV file found in the zip archive.")
    else:
        return pd.read_csv(io.BytesIO(content))


def get_pdf_text_from_location(location: str) -> str:
    """Download a PDF from a URL or a local file path and extract its text content."""
    if location.startswith('http'):
        response = requests.get(location)
        response.raise_for_status()
        content = response.content
    else:
        with open(location, 'rb') as f:
            content = f.read()

    with io.BytesIO(content) as f:
        reader = PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text
