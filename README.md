# PitchDeck-Agents

Multi-agent AI that turns startup ideas into investor-ready pitch decks. 8 specialized agents on Google ADK & Gemini—from idea to deck with real-time market research.

## Overview

PitchDeck-Agents is a multi-agent AI pipeline built on [Google Agent Development Kit (ADK)](https://google.github.io/adk-docs/) and Gemini. You describe your startup idea, and a coordinated team of 8 specialized AI agents researches the market in real-time, analyzes the competitive landscape, and produces a complete 10-slide investor pitch deck.

## Architecture

The system uses a `SequentialAgent` orchestrator that runs 8 specialized agents in order, with each agent passing its output to the next via shared session state.

```
User Idea
    │
    ▼
┌─────────────────────────────────────────────────────┐
│           Pitch Deck Orchestrator                   │
│              (SequentialAgent)                      │
│                                                     │
│  1. 🔍 Idea Analyzer                               │
│     └─ Extracts problem, solution, target market   │
│                                                     │
│  2. 📊 Market Researcher          [google_search]  │
│     └─ TAM/SAM/SOM, CAGR, trends                  │
│                                                     │
│  3. 🏆 Competitive Analyst        [google_search]  │
│     └─ Competitors, positioning, moats             │
│                                                     │
│  4. 💡 Value Proposition Creator                   │
│     └─ One-liner, differentiators, "why now"       │
│                                                     │
│  5. 💰 Business Model Designer                     │
│     └─ Revenue streams, pricing, GTM, unit econ    │
│                                                     │
│  6. 📈 Financial Projections Analyst               │
│     └─ 5-year forecast, funding ask, use of funds  │
│                                                     │
│  7. 👥 Team & Traction Advisor                     │
│     └─ Team profile, KPIs, milestone roadmap       │
│                                                     │
│  8. 📋 Pitch Deck Compiler                         │
│     └─ 10-slide investor deck + objection handling │
└─────────────────────────────────────────────────────┘
    │
    ▼
Complete Investor Pitch Deck
```

## Prerequisites

- Python 3.11+
- A Google API Key with Gemini access ([get one here](https://aistudio.google.com/app/apikey))

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/HarshaVardhanMannem/PitchDeck-Agents.git
cd PitchDeck-Agents
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

## Usage

### Interactive Web UI (Recommended)

Launch the ADK web interface to chat with the agent interactively:

```bash
adk web
```

Then open [http://localhost:8000](http://localhost:8000) in your browser, select **pitch_deck_orchestrator**, and describe your startup idea.

### Command Line

Run the agent pipeline directly from the terminal:

```bash
adk run pitch_deck_agents
```

### Example Prompt

```
I'm building a B2B SaaS platform that uses AI to automate employee onboarding for
mid-market companies (500-5000 employees). HR teams currently spend 40+ hours per
new hire on manual paperwork, system provisioning, and training coordination. Our
platform integrates with existing HRIS systems and reduces onboarding time by 70%
while improving new hire satisfaction scores. We have 3 design partners signed up
and are raising a $2M seed round.
```

## Output

The pipeline produces a complete **10-slide investor pitch deck** covering:

| Slide | Content |
|-------|---------|
| 1 | Cover — Company name, tagline, round |
| 2 | Problem — Pain point, target customer, cost of problem |
| 3 | Solution — Product overview, key features, "aha moment" |
| 4 | Market Opportunity — TAM/SAM/SOM, growth rate, "why now" |
| 5 | Business Model — Revenue streams, pricing, unit economics |
| 6 | Traction — Key metrics, milestones, customer proof |
| 7 | Competitive Landscape — Positioning matrix, moat |
| 8 | Team — Founders, advisors, key hires |
| 9 | Financial Projections — 5-year forecast, burn, break-even |
| 10 | The Ask — Funding amount, use of funds, milestones |

Plus: executive summary, top investor objections & responses, and next steps.

## Project Structure

```
PitchDeck-Agents/
├── pitch_deck_agents/
│   ├── __init__.py
│   ├── agent.py                          # Root SequentialAgent orchestrator
│   └── sub_agents/
│       ├── __init__.py
│       ├── idea_analyzer.py              # Agent 1: Startup idea analysis
│       ├── market_researcher.py          # Agent 2: Real-time market research
│       ├── competitive_analyst.py        # Agent 3: Competitive intelligence
│       ├── value_proposition_creator.py  # Agent 4: Value proposition crafting
│       ├── business_model_designer.py    # Agent 5: Business model design
│       ├── financial_projections_analyst.py  # Agent 6: Financial modeling
│       ├── team_traction_advisor.py      # Agent 7: Team & traction
│       └── pitch_deck_compiler.py        # Agent 8: Final deck compilation
├── requirements.txt
├── .env.example
└── README.md
```

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Agent Framework | [Google Agent Development Kit (ADK)](https://google.github.io/adk-docs/) |
| LLM | Gemini 2.0 Flash |
| Real-time Research | Google Search (via ADK built-in tool) |
| Orchestration | `SequentialAgent` (ADK) |
| Language | Python 3.11+ |

## How It Works

1. **You provide** a startup idea description (a few sentences to a paragraph)
2. **Agent 1** structures the idea into problem, solution, market, and key assumptions
3. **Agents 2 & 3** conduct real-time web research to size the market and map the competitive landscape
4. **Agents 4–7** synthesize the research into value proposition, business model, financial projections, and team guidance
5. **Agent 8** assembles everything into a polished, slide-by-slide pitch deck with investor objection prep

Each agent's output is stored in the session state and made available to subsequent agents, ensuring a coherent, data-driven narrative throughout the deck.
