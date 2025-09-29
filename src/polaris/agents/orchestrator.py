"""
Orchestrator agent that decides which agent to call.
"""

import json
import ollama

from polaris.agents.base import BaseAgent
from polaris.agents.data_source import DataSourceAgent
from polaris.agents.codebook import CodebookAgent
from polaris.services.data_loader import load_csv
from polaris.services import data_analysis

class OrchestratorAgent(BaseAgent):
    """Orchestrator agent that decides which agent to call."""

    def __init__(self):
        self.data_source_agent = DataSourceAgent()
        self.codebook_agent = CodebookAgent()

    def run(self, prompt: str, **kwargs) -> str:
        """Run the agent."""
        
        sources = kwargs.get("sources", [])
        model = kwargs.get("model", "llama3")

        if not sources:
            return "Please select a data source to start the analysis."

        # 1. Get data path
        csv_path = self.data_source_agent.run(sources)
        if csv_path is None:
            return "Error: Could not get the data path from the selected source."

        # 2. Load data
        df = load_csv(csv_path)
        if df is None:
            return "Error: Could not load data from the selected source."

        # 3. Get codebook context
        codebook_context = self.codebook_agent.run(sources)

        # 4. Define available functions
        available_functions = {
            "get_total_fatalities": data_analysis.get_total_fatalities,
        }

        # 5. Create the prompt for function calling
        agent_prompt = f"""
        You are a data analyst. You are given a user's question and a list of available functions.
        Your task is to choose the best function to answer the user's question and provide the necessary parameters.
        The available functions are:
        - get_total_fatalities(df, country, year): Get the total number of fatalities for a given country and year.

        {codebook_context}

        The user's question is:
        {prompt}

        Respond with a JSON object containing the function name and the parameters. For example:
        {{"function": "get_total_fatalities", "parameters": {{"country": "Syria", "year": 2020}}}}
        """

        # 6. Call the LLM to get the function call
        response = ollama.chat(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": agent_prompt,
                },
            ],
        )
        function_call_json = response["message"]["content"]
        print(f"---LLM response---\n{function_call_json}\n---")

        # 7. Parse the function call and execute the function
        try:
            # Extract the JSON object from the response.
            if "```" in function_call_json:
                function_call_json = function_call_json.split("```")[1]
                if function_call_json.lower().startswith("json"): 
                    function_call_json = function_call_json[4:]
            
            function_call = json.loads(function_call_json)
            function_name = function_call["function"]
            parameters = function_call["parameters"]

            if function_name in available_functions:
                result = available_functions[function_name](df, **parameters)
                return str(result)
            else:
                return "Error: The chosen function is not available."

        except (json.JSONDecodeError, KeyError):
            return "Error: Could not parse the function call from the LLM."
