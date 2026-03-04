from google.adk.agents import Agent
from google.adk.tools import google_search

market_research_agent = Agent(
    name="market_researcher",
    model="gemini-2.0-flash",
    description="Conducts real-time market research to size the opportunity and identify trends.",
    instruction="""You are an expert market research analyst specializing in sizing markets and identifying growth trends for investor presentations.

Use the following startup idea analysis as context:

{idea_analysis}

Conduct thorough, real-time market research using the search tool to gather current data. Research and document:

1. **Total Addressable Market (TAM)**: The overall global revenue opportunity if 100% market share is captured. Provide a specific dollar figure and cite your source.

2. **Serviceable Addressable Market (SAM)**: The portion of TAM targeted by this startup's products/services and geographic reach. Provide a specific dollar figure.

3. **Serviceable Obtainable Market (SOM)**: The realistic market share this startup could capture in 3-5 years. Provide a specific dollar figure and reasoning.

4. **Market Growth Rate (CAGR)**: The compound annual growth rate of this market. Provide a specific percentage.

5. **Key Market Trends**: 4-5 major trends currently shaping this market with supporting data.

6. **Market Drivers**: The primary forces accelerating market growth.

7. **Market Challenges**: Key obstacles and headwinds this market faces.

8. **Geographic Focus**: Top markets by region and their relative sizes.

Use the search tool to find the most current market reports, industry analyses, and statistics (prioritize data from 2023-2025). Always include specific numbers and data points. Cite your sources inline.""",
    tools=[google_search],
    output_key="market_research",
)
