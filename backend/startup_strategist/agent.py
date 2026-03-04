import os
import uuid
from google.adk.agents import Agent, SequentialAgent, LoopAgent
from google.adk.tools import google_search
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


# Agent 1 - Clarify Idea Agent
clarify_idea_agent = Agent(
    name="clarify_idea_agent",
    model="gemini-2.0-flash",
    instruction="""
    You are a startup strategist. Clarify the user's business idea and rephrase it to be investor-ready.
    Keep it concise but compelling. Your goal is to define the startup vision in 1-2 sentences.
    Return only the refined idea, nothing else.
    """,
    output_key="refined_idea"
)

# Agent 2 - Problem Statement Agent
problem_statement_agent = Agent(
    name="problem_statement_agent",
    model="gemini-2.0-flash",
    tools=[google_search],
    instruction="""
    You have access to this refined idea: {refined_idea}
    
    Define the problem that this startup idea is solving. Focus on the pain points, scale of the problem, and who faces it.
    Research current market data if needed using google_search.
    Output just the problem statement in 2-3 clear sentences.
    """,
    output_key="problem"
)

# Agent 3 - Target Customer Agent
target_customer_agent = Agent(
    name="target_customer_agent",
    model="gemini-2.0-flash",
    tools=[google_search],
    instruction="""
    You have access to: {refined_idea}
    
    Identify the ideal target customer for this startup idea.
    Use demographic and behavioral characteristics. Who exactly would use this? Avoid generic audiences.
    Research market segments if needed using google_search.
    Provide a specific customer profile.
    """,
    output_key="customer"
)

# Agent 4 - MVP Planner Agent
mvp_planner_agent = Agent(
    name="mvp_planner_agent",
    model="gemini-2.0-flash",
    instruction="""
    You have access to:
    - Idea: {refined_idea}
    - Problem: {problem}
    - Target Customer: {customer}
    
    Based on this information, propose a simple MVP (Minimum Viable Product).
    List the key features and the simplest version of the product that can be shipped in 4-6 weeks.
    Focus on core functionality that addresses the main problem.
    """,
    output_key="mvp"
)

# Agent 5 - Competitor Analysis Agent
competitor_analysis_agent = Agent(
    name="competitor_analysis_agent",
    model="gemini-2.0-flash",
    tools=[google_search],
    instruction="""
    You have access to: {refined_idea}
    
    Find the top 3 existing competitors for this idea using google_search.
    Summarize their key features and how they solve the same problem.
    Output a short list with company names, brief descriptions, and their main strengths.
    """,
    output_key="competitors"
)

# Agent 6 - Monetization Agent
monetization_agent = Agent(
    name="monetization_agent",
    model="gemini-2.0-flash",
    instruction="""
    You have access to:
    - Idea: {refined_idea}
    - Competitors: {competitors}
    
    Propose 2-3 realistic ways this idea can make money. Be specific: subscriptions, transaction fees, licensing, freemium, etc.
    Consider what competitors are doing and identify potential revenue opportunities.
    Provide clear revenue model explanations.
    """,
    output_key="monetization"
)

# Agent 7 - Go-to-Market Agent
go_to_market_agent = Agent(
    name="go_to_market_agent",
    model="gemini-2.0-flash",
    instruction="""
    You have access to:
    - MVP: {mvp}
    - Target Customer: {customer}
    
    Propose a Go-To-Market (GTM) strategy focused on acquiring the first 100 users.
    Include specific channels (e.g., Reddit communities, LinkedIn, cold emails, content marketing).
    Provide actionable steps and timeline for customer acquisition.
    """,
    output_key="gtm"
)

# Agent 8 - Pitch Deck Agent
pitch_deck_agent = Agent(
    name="pitch_deck_agent",
    model="gemini-2.0-flash",
    instruction="""
    You have access to all previous outputs:
    - Refined Idea: {refined_idea}
    - Problem: {problem}
    - Target Customer: {customer}
    - MVP: {mvp}
    - Competitors: {competitors}
    - Monetization: {monetization}
    - GTM Strategy: {gtm}
    
    Create a comprehensive pitch deck outline using all this information.
    Structure it as a professional investor pitch with clear sections:
    1. Problem & Opportunity
    2. Solution (MVP)
    3. Target Market & Customer
    4. Competitive Landscape
    5. Revenue Model
    6. Go-to-Market Strategy
    7. Next Steps
    
    Make it investor-ready and compelling.
    """,
    output_key="pitch_deck"
)

# Loop Agent 1 - Validation Loop Agent
validation_agent = Agent(
    name="validation_agent",
    model="gemini-2.0-flash",
    instruction="""
    You are a validation specialist. Review the current analysis and identify any gaps or areas that need refinement.
    
    Current analysis includes:
    - Refined Idea: {refined_idea}
    - Problem: {problem}
    - Target Customer: {customer}
    - MVP: {mvp}
    - Competitors: {competitors}
    - Monetization: {monetization}
    - GTM Strategy: {gtm}
    - Pitch Deck: {pitch_deck}
    
    Evaluate the completeness and quality of each component. Identify:
    1. Missing critical information
    2. Inconsistencies between components
    3. Areas that need more detail or research
    4. Potential red flags or weak points
    
    If you find significant issues that need addressing, provide specific feedback.
    If the analysis is comprehensive and ready, indicate it's complete.
    """,
    output_key="validation_feedback"
)

market_research_agent = Agent(
    name="market_research_agent",
    model="gemini-2.0-flash",
    tools=[google_search],
    instruction="""
    You are a market research specialist. Conduct market research to validate and refine the startup concept.
    
    Current concept: {refined_idea}
    Target market: {customer}
    Problem: {problem}
    Validation feedback: {validation_feedback}
    
    Research and validate:
    1. Market size and growth potential
    2. Customer pain points and willingness to pay
    3. Competitive landscape depth
    4. Market trends and timing
    5. Regulatory or technical barriers
    
    Use google_search to find current market data, trends, and insights.
    Focus on addressing any gaps identified in the validation feedback.
    """,
    output_key="market_insights"
)

strategy_refinement_agent = Agent(
    name="strategy_refinement_agent",
    model="gemini-2.0-flash",
    instruction="""
    You are a strategy refinement specialist. Improve the startup strategy based on validation feedback and market insights.
    
    Current strategy components:
    - MVP: {mvp}
    - Monetization: {monetization}
    - GTM Strategy: {gtm}
    - Market Insights: {market_insights}
    - Validation Feedback: {validation_feedback}
    
    Review and refine:
    1. MVP feasibility and timeline
    2. Revenue model viability
    3. GTM strategy effectiveness
    4. Risk mitigation strategies
    5. Success metrics and KPIs
    
    Provide specific improvements and refinements to the strategy.
    """,
    output_key="refined_strategy"
)

# Create Loop Agent 1 - Validation Loop
validation_loop_agent = LoopAgent(
    name="validation_loop_agent",
    description="Iteratively validates and refines the startup analysis",
    sub_agents=[validation_agent, market_research_agent, strategy_refinement_agent],
    max_iterations=3
)

# Agent 9 - Final Synthesis Agent
final_synthesis_agent = Agent(
    name="final_synthesis_agent",
    model="gemini-2.0-flash",
    instruction="""
    You are a final synthesis specialist. Create a comprehensive, polished final output that incorporates all iterations and refinements.
    
    You have access to all outputs including loop iterations:
    - Original Analysis: {refined_idea}, {problem}, {customer}, {mvp}, {competitors}, {monetization}, {gtm}, {pitch_deck}
    - Loop Iterations: {validation_feedback}, {market_insights}, {refined_strategy}
    
    Create a final, investor-ready startup strategy document that includes:
    1. Executive Summary
    2. Problem & Market Opportunity
    3. Solution & MVP
    4. Target Market & Customer Validation
    5. Competitive Analysis
    6. Revenue Model & Financial Projections
    7. Go-to-Market Strategy
    8. Risk Assessment & Mitigation
    9. Success Metrics & Milestones
    10. Investment Ask & Use of Funds
    
    Make this document comprehensive, professional, and ready for investor presentation.
    """,
    output_key="final_strategy"
)

# Agent 10 - Memory Agent
memory_agent = Agent(
    name="memory_agent",
    model="gemini-2.0-flash",
    instruction="""
    You have access to all previous outputs and iterations:
    - Original Analysis: {refined_idea}, {problem}, {customer}, {mvp}, {competitors}, {monetization}, {gtm}, {pitch_deck}
    - Loop Iterations: {validation_feedback}, {market_insights}, {refined_strategy}
    - Final Strategy: {final_strategy}
    
    Create a comprehensive memory summary of this startup analysis session, including:
    1. Key insights and learnings
    2. Iterations and refinements made
    3. Critical decisions and rationale
    4. Areas for future research or validation
    5. Success factors and potential challenges
    
    This memory will be used for future reference and to avoid regenerating similar analyses.
    """,
    output_key="memory"
)

# Create the main Sequential Agent that ADK web will use
root_agent = SequentialAgent(
    name="startup_strategist",
    description="A comprehensive startup strategist that transforms business ideas into investor-ready pitch decks through systematic analysis with iterative refinement loops.",
    sub_agents=[
        clarify_idea_agent,
        problem_statement_agent,
        target_customer_agent,
        mvp_planner_agent,
        competitor_analysis_agent,
        monetization_agent,
        go_to_market_agent,
        pitch_deck_agent,
        validation_loop_agent,
        final_synthesis_agent,
        memory_agent,
    ]
)

