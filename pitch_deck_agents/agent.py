from google.adk.agents import SequentialAgent

from .sub_agents import (
    idea_analyzer_agent,
    market_research_agent,
    competitive_analyst_agent,
    value_proposition_agent,
    business_model_agent,
    financial_projections_agent,
    team_traction_agent,
    pitch_deck_compiler_agent,
)

root_agent = SequentialAgent(
    name="pitch_deck_orchestrator",
    description=(
        "Orchestrates 8 specialized AI agents to transform a startup idea into a "
        "complete, investor-ready pitch deck with real-time market research."
    ),
    sub_agents=[
        idea_analyzer_agent,        # Agent 1: Analyze the startup idea
        market_research_agent,      # Agent 2: Real-time market sizing & trends
        competitive_analyst_agent,  # Agent 3: Competitive landscape research
        value_proposition_agent,    # Agent 4: Craft unique value proposition
        business_model_agent,       # Agent 5: Design business model & GTM
        financial_projections_agent,  # Agent 6: Build financial projections
        team_traction_agent,        # Agent 7: Team structure & traction
        pitch_deck_compiler_agent,  # Agent 8: Compile the final pitch deck
    ],
)
