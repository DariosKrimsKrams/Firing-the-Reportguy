# Install dependencies


# Mount Google Drive
#from google.colab import drive
import pandas as pd
import openai
import numpy as np

#drive.mount('/content/drive')

# 🔁 Set your CSV file path here
#csv_path = '/content/drive/MyDrive/your_folder/your_file.csv'
csv_path = '/content/test.csv'
df = pd.read_csv(csv_path)

# ✅ Sample 100 rows evenly spaced throughout the dataset
sample_size = min(100, len(df))
indices = np.linspace(0, len(df) - 1, sample_size, dtype=int)
sample_df = df.iloc[indices]

# ✅ Convert sample to CSV string
sample_csv = sample_df.to_csv(index=False)

# ✅ Calculate correlation matrix for numeric columns
corr_matrix = df.corr(numeric_only=True).round(2).to_string()

# ✅ Get column data types
column_types = {col: str(dtype) for col, dtype in df.dtypes.items()}
column_types_str = json.dumps(column_types, indent=2)

# ✅ Construct the GPT prompt
prompt1 = f"""
You are a data analyst.

You are given a representative sample of a dataset. This sample has been taken evenly across the full dataset to preserve its structure and trends.

Below is the sample (100 rows):
{sample_csv}

Below is the correlation matrix of numerical columns:
{corr_matrix}

And here are the column data types:
{column_types_str}

Please do the following:
1. Provide a short and descriptive **title** summarizing the overall theme of the dataset.
2. Write a 2–3 sentence **overview** of the dataset structure and key features.
3. Give a bullet list of **6–7 trends, patterns, correlations, or anomalies** based on this data. Focus on numeric variation, relationships, missing data, value distributions, or unusual behaviors.
"""

#----------------------
csv_text = df.to_csv(index=False)
prompt2 = f"""
You are a professional data analyst.

Here is the full dataset in CSV format:
{csv_text}

Please do the following:
1. Provide a clear and descriptive **title** for the dataset.
2. Write a **2–3 sentence overview** describing what this dataset is about and how it's structured.
3. Identify and explain **6–7 key trends, correlations, or patterns** based on this data. You may comment on:
   - Common value distributions
   - Relationships between variables
   - Outliers or anomalies
   - Columns with high or low variability
   - Anything unusual or interesting

Please write clearly and professionally, as if explaining your findings to a colleague who hasn’t seen the data.
"""

prompt3 =  f"""
You are a data analyst tasked with writing a statistical summary report based on the following dataset:

{csv_text}

Write the report using the following structure:
1. Begin with a concise, fact-driven paragraph that summarizes major numerical trends in the data. The tone should be formal, neutral, and impersonal — like a government or UN report. Avoid phrases like "this dataset" or "we found".
2. After the summary paragraph, provide a bullet list of 6–7 key observations. Each bullet should present one notable statistic, regional variation, or change pattern in a factual and detached tone.
3. Use numbers, units, and comparisons (e.g. month-on-month change, percentage differences, regional rankings) whenever possible.
4. Avoid any personal or analytical language — present the information as statistical facts.

The goal is to present a data-driven summary similar to a humanitarian bulletin or economic trends report.
"""


prompt4 = f"""
You are a professional statistical reporter. You are tasked with writing a formal, factual report using quantitative information extracted from the following data:

{csv_text}

Write a concise report with the following structure:

1. Start with a paragraph that presents the main numerical trends, facts, and comparisons. Do not refer to the dataset or say that data was analyzed — present the information as real-world observations or statistics.
2. Follow this with a bullet list of 6–7 specific observations. Each bullet should report a number, ranking, pattern, or change in a neutral, factual tone.
3. Use percentages, ranks, comparisons, and figures where appropriate.
4. Do not use words like "the dataset", "data shows", "analysis reveals", or "according to the data".
5. Present it as if this information is being directly communicated to stakeholders or the public.

Your tone should match that of official UN or economic trend bulletins — factual, impersonal, and clear.
"""


# ✅ Set your OpenAI API key
client = openai.OpenAI(api_key="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")  # 🔐 Replace with your API key

# ✅ Query the OpenAI Chat API
response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",  # Or "gpt-3.5-turbo" if GPT-4 is unavailable
    messages=[
        {"role": "system", "content": "You are a helpful data analyst."},
        {"role": "user", "content": prompt4}
    ],
    temperature=0.5,
    max_tokens=1000
)

# ✅ Print GPT's response
print("\n🧠 GPT Analysis:")
print(response.choices[0].message.content.strip())
