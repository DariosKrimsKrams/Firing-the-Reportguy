import openai
import os
from dotenv import load_dotenv
import pandas as pd
from typing import Callable, Dict

prompt_template = """
You are a professional trends reporter working for a humanitarian or economic monitoring agency.
Using the information below, write a formal, fact-based situation update. This report should follow the structure and tone of official UN or humanitarian bulletins.


{csv_text}


Follow these instructions carefully:
1. Begin with a title followed by short **narrative paragraph** that summarizes the key overall trends in the observed period. Embed important figures and percentage changes smoothly in the text. Use neutral, formal language.
2. Then, write a bullet list of **6–7 factual observations**. Each bullet must:
   - Focus on one specific trend or comparison
   - Include **numerical values**
   - Include a **date or date range** (e.g., “in January 2024”, “from Feb 2023 to April 2024”, “as of March 2024”)
   - Present the information as a **real-world fact**, not as an analysis
3. Avoid phrases like “the data shows”, “the dataset contains”, or “analysis reveals”. This is not a data report — it is a factual summary of real-world conditions, written for policymakers, donors, and field teams.
4. You may refer to governorates, districts, or markets by name where relevant. Do not mention the source of the data or the existence of a dataset.
5. Be concise, objective, and professional. Focus on what changed, when it changed, and where it changed.
The report should read like a situational overview — useful for briefing stakeholders on recent market or accessibility trends.
"""

class Model:
    def __init__(self, model_name: str = "gpt-4.5-preview"):
        load_dotenv(override=True)
        self.client = openai.OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
        )
        self.model_name = model_name

        self.function_callables : Dict[str, Callable] = {}
        self.function_dicts : Dict[str, Dict] = {}

    def register_function_call(self, function_dict: Dict, function : Callable):
        """
        See: https://platform.openai.com/docs/guides/function-calling?api-mode=responses#token-usage

        Example:
        tools = [{
    "type": "function",
    "name": "get_weather",
    "description": "Get current temperature for provided coordinates in celsius.",
    "parameters": {
        "type": "object",
        "properties": {
            "latitude": {"type": "number"},
            "longitude": {"type": "number"}
        },
        "required": ["latitude", "longitude"],
        "additionalProperties": False
    },
    "strict": True
}]
        """
        self.function_callables[function_dict["name"]] = function
        self.function_dicts[function_dict["name"]] = function_dict

    def run_for_df(self, df: pd.DataFrame):
        # Convert DataFrame to CSV format
        csv_text = df.to_csv(index=False)

        formatted_prompt = prompt_template.format(csv_text=csv_text)
        # Query the OpenAI Chat API
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "user", "content": formatted_prompt}
            ],
            # functions=list(self.function_dicts.values()),
            temperature=0.0,
            max_tokens=1500,
        )

        print(response)

        return response.choices[0].message.content