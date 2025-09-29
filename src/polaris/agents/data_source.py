"""
Agent for loading data from data sources.
"""

import pandas as pd
import os
import urllib.request
import zipfile

from polaris.agents.base import BaseAgent
from polaris.core.config import load_data_sources

class DataSourceAgent(BaseAgent):
    """Agent for loading data from data sources."""

    def run(self, sources: list[str], **kwargs) -> str:
        """Run the agent and return the path to the csv file."""

        all_sources = load_data_sources()
        selected_sources = [s for s in all_sources if s.name in sources]

        # For now, we only support one data source at a time.
        if selected_sources:
            source = selected_sources[0]
            
            # Create a path to the local data file.
            file_name = source.url.split('/')[-1]
            local_path = os.path.join("src", "polaris", "data", file_name)

            # Check if the file exists.
            if not os.path.exists(local_path):
                print(f"Downloading data from: {source.url}")
                urllib.request.urlretrieve(source.url, local_path)
            
            if local_path.endswith('.zip'):
                with zipfile.ZipFile(local_path, 'r') as zip_ref:
                    # Find the first CSV file in the zip archive
                    csv_file_name = next((f for f in zip_ref.namelist() if f.endswith('.csv')), None)
                    if csv_file_name:
                        # Extract the file with a new name based on the data source name.
                        extracted_file_path = os.path.join("src", "polaris", "data", f"{source.name}.csv")
                        with zip_ref.open(csv_file_name) as zf, open(extracted_file_path, 'wb') as f:
                            f.write(zf.read())
                        return extracted_file_path
                    else:
                        raise ValueError("No CSV file found in the zip archive.")
            else:
                return local_path
        
        return None
