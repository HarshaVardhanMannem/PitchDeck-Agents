# Startup Strategist Agent

A comprehensive AI-powered startup strategist that transforms raw business ideas into investor-ready pitch decks using an 8-agent sequential pipeline built on Google ADK and Gemini 2.0 Flash.

## 🚀 Features

- **8-Agent Sequential Pipeline**: Specialized agents for each aspect of startup development
- **Real-Time Market Research**: Google Search integration for current market data
- **Comprehensive Analysis**: From idea clarification to pitch deck generation
- **Professional Output**: Investor-ready documentation and presentations
- **Robust Architecture**: Error handling and quality assurance

## 📋 Prerequisites

- Python 3.11+
- Google ADK installed and configured
- Google API key with access to:
  - Gemini 2.0 Flash
  - Google Search API
- Stable internet connection

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd adk-project
   ```

2. **Set up virtual environment**:
   ```bash
   python -m venv adkenv
   source adkenv/bin/activate  # On Windows: adkenv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install google-adk python-dotenv
   ```

4. **Configure environment variables**:
   Create a `.env` file in the `harsha-vardhan-mannem/src/startup_strategist` directory:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## 🎯 Running with ADK Web Interface

### Method 1: ADK Web Interface (Recommended)

1. **Navigate to your project directory**:
   ```bash
   cd harsha-vardhan-mannem/src
   ```

2. **Start the ADK web interface**:
   ```bash
   adk web
   ```

3. **Access the web interface**:
   - Open your browser and go to `http://localhost:8080`
   - You'll see the ADK web interface with available agents

4. **Select the Startup Strategist Agent**:
   - Look for the agent named "startup_strategist"
   - Click on it to open the agent interface

5. **Run your startup idea**:
   - Enter your business idea in the input field
   - Click "Run" to start the analysis
   - Watch as the 8-agent pipeline processes your idea


3. **Enter your business idea when prompted**

## 📁 Project Structure

```
adk-project/
├── adkenv/                          # Virtual environment
├── harsha-vardhan-mannem/           # Main project directory
│   ├── src/                         # Source code directory
│   │   └── startup_strategist/      # Agent implementation
│   │       ├── agent.py             # Main agent file
│   │       └── .env                 # Environment variables
│   ├── README.md                    # Project documentation
│   ├── ARCHITECTURE.md              # System architecture
│   ├── EXPLANATION.md               # Technical explanation
│   └── DEMO.md                      # Demo documentation
└── README.md                        # Root README
```

## 🏗️ Agent Architecture

The system uses 8 specialized agents in sequence:

1. **Clarify Idea Agent**: Refines raw ideas into clear concepts
2. **Problem Statement Agent**: Identifies real-world problems
3. **Target Customer Agent**: Defines ideal user personas
4. **MVP Planner Agent**: Designs minimum viable products
5. **Competitor Analysis Agent**: Researches market competition
6. **Monetization Agent**: Develops revenue strategies
7. **Go-to-Market Agent**: Creates customer acquisition plans
8. **Pitch Deck Agent**: Generates investor presentations

## 📊 Example Usage

### Input Example:
```
"I want to build an AI-powered meal planning app"
```

### Output Includes:
- **Refined Business Concept**: Clear, investor-ready description
- **Problem Analysis**: Market problems and significance
- **Target Customer Profile**: Demographics and behavior
- **MVP Strategy**: 4-6 week development plan
- **Competitor Analysis**: Top competitors and differentiation
- **Revenue Model**: 2-3 monetization strategies
- **Go-to-Market Plan**: First 100 customer acquisition
- **Pitch Deck**: Complete investor presentation

## 🔧 Configuration

### Environment Variables
- `GOOGLE_API_KEY`: Your Google API key for Gemini and Search
- `ADK_PROJECT_ID`: Your Google Cloud project ID (optional)

### Agent Customization
You can modify agent instructions in `harsha-vardhan-mannem/src/startup_strategist/agent.py`:
- Adjust agent prompts for different industries
- Add new tools for enhanced capabilities
- Modify output formats for specific needs

## 🚨 Troubleshooting

### Common Issues:

1. **ADK Web Interface Not Starting**:
   ```bash
   # Check if ADK is properly installed
   adk --version
   
   # Reinstall if needed
   pip install --upgrade google-adk
   ```

2. **API Key Errors**:
   - Verify your Google API key is valid
   - Ensure the key has access to Gemini and Search APIs
   - Check that the `.env` file is in the correct location: `harsha-vardhan-mannem/src/startup_strategist/.env`

3. **Import Errors**:
   ```bash
   # Reinstall dependencies
   pip install -r requirements.txt
   ```

4. **Network Issues**:
   - Ensure stable internet connection
   - Check firewall settings
   - Verify Google API quotas

5. **Wrong Directory Issues**:
   - Make sure you're in the correct directory: `harsha-vardhan-mannem/src/`
   - Verify the agent file exists: `startup_strategist/agent.py`
   - Make sure the name of the SequentialAgent is startup_strategist same as your folder name and also make sure the variable name is root_agent 

## 📈 Performance Tips

- **Use specific ideas**: More detailed inputs yield better results
- **Stable internet**: Required for real-time market research
- **Monitor API usage**: Track your Google API quota usage
- **Cache results**: The system remembers previous analyses

## 📚 Documentation

- **README.md**: This file - setup and usage instructions
- **ARCHITECTURE.md**: Detailed system architecture and design
- **EXPLANATION.md**: Technical explanation of agent behavior
- **DEMO.md**: Demo video guide and script


## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
- Check the troubleshooting section above
- Review the ARCHITECTURE.md for technical details
- Consult the EXPLANATION.md for system behavior
- Open an issue on GitHub

---

 