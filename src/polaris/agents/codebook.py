"""
Agent for parsing and understanding codebooks.
"""

import os
import urllib.request

from polaris.agents.base import BaseAgent
from polaris.core.config import load_data_sources
from polaris.services.data_loader import get_pdf_text_from_location

class CodebookAgent(BaseAgent):
    """Agent for parsing and understanding codebooks."""

    def run(self, sources: list[str], **kwargs) -> str:
        """Run the agent."""

        all_sources = load_data_sources()
        selected_sources = [s for s in all_sources if s.name in sources]

        codebook_context = ""

        # For now, we only support one data source at a time.
        if selected_sources:
            source = selected_sources[0]
            if source.codebook_url:
                # Create a path to the local codebook file.
                file_name = source.codebook_url.split('/')[-1]
                local_path = os.path.join("src", "polaris", "data", file_name)

                # Check if the file exists.
                if not os.path.exists(local_path):
                    print(f"Downloading codebook from: {source.codebook_url}")
                    urllib.request.urlretrieve(source.codebook_url, local_path)
                
                print(f"Loading codebook from: {local_path}")
                codebook_context = get_pdf_text_from_location(local_path)

            elif "ucdp" in source.name.lower():
                codebook_context = """
                The UCDP Georeferenced Event Dataset has the following relevant columns:
                - country: The country where the event took place.
                - year: The year of the event.
                - best: The best estimate of the total number of fatalities.
                - high: The high estimate of the total number of fatalities.
                - low: The low estimate of the total number of fatalities.
                """
        
        return codebook_context
