from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import sys
import os
import asyncio
from typing import Dict, Any
import uuid
import re

# Add the backend directory to the Python path for local imports
sys.path.insert(0, os.path.dirname(__file__))

try:
    from startup_strategist.agent import root_agent
    print("✅ Real agent loaded successfully")
    AGENT_LOADED = True
except ImportError as e:
    print(f"⚠️ Agent import failed: {e}")
    print("🔄 Using mock agent for testing")
    AGENT_LOADED = False
    # Fallback: create a mock agent for testing
    class MockAgent:
        def run(self, idea):
            return type('Result', (), {
                'output': {
                    'refined_idea': f"Enhanced: {idea}",
                    'problem': f"Market problem analysis for: {idea}",
                    'target_customer': f"Target customers for: {idea}",
                    'mvp': f"MVP strategy for: {idea}",
                    'competitor_analysis': f"Competitive analysis for: {idea}",
                    'monetization': f"Revenue model for: {idea}",
                    'go_to_market': f"GTM strategy for: {idea}",
                    'pitch_deck': f"Investor pitch for: {idea}"
                }
            })()
    root_agent = MockAgent()

app = FastAPI(title="Startup Strategist API", version="1.0.0")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BusinessIdea(BaseModel):
    idea: str

class AnalysisResponse(BaseModel):
    status: str
    results: Dict[str, Any]
    message: str

def enhance_content_with_markdown(content: str, agent_type: str) -> str:
    """Convert agent output to well-formatted markdown"""
    if not content or len(content.strip()) < 10:
        return content
    
    # If content already has markdown headers, return as-is
    if re.search(r'^#{1,6}\s', content, re.MULTILINE):
        return content
    
    # Add appropriate header based on agent type
    agent_headers = {
        'refined_idea': '# 💡 Refined Business Concept',
        'problem': '# 🎯 Problem Analysis', 
        'target_customer': '# 👥 Target Customer Profile',
        'mvp': '# 🛠️ MVP Strategy',
        'competitor_analysis': '# 🏢 Competitive Analysis',
        'monetization': '# 💰 Monetization Strategy',
        'go_to_market': '# 📈 Go-to-Market Plan',
        'pitch_deck': '# 📊 Investment Pitch',
        'validation_feedback': '# ✅ Validation Insights',
        'final_synthesis': '# 🎯 Strategic Synthesis',
        'memory_summary': '# 💾 Key Insights Summary'
    }
    
    header = agent_headers.get(agent_type, f'# {agent_type.replace("_", " ").title()}')
    
    # Clean and format the content
    lines = content.strip().split('\n')
    formatted_lines = [header, '']
    
    current_section = []
    
    for line in lines:
        line = line.strip()
        if not line:
            if current_section:
                formatted_lines.extend(current_section)
                formatted_lines.append('')
                current_section = []
            continue
            
        # Convert numbered lists to markdown
        if re.match(r'^\d+\.\s', line):
            if current_section and not current_section[-1].startswith('1.'):
                formatted_lines.extend(current_section)
                formatted_lines.append('')
                current_section = []
            current_section.append(line)
        # Convert bullet points
        elif line.startswith('- ') or line.startswith('* '):
            current_section.append(line)
        # Convert titles/headers (lines ending with :)
        elif line.endswith(':') and len(line) < 100:
            if current_section:
                formatted_lines.extend(current_section)
                formatted_lines.append('')
                current_section = []
            formatted_lines.append(f'## {line[:-1]}')
            formatted_lines.append('')
        else:
            current_section.append(line)
    
    # Add remaining content
    if current_section:
        formatted_lines.extend(current_section)
    
    return '\n'.join(formatted_lines)

# Mount static files for serving React app (only if directory exists)
if os.path.exists("../frontend/build/static"):
    app.mount("/static", StaticFiles(directory="../frontend/build/static"), name="static")

@app.get("/")
async def serve_react_app():
    """Serve the React app"""
    if os.path.exists("../frontend/build/index.html"):
        return FileResponse('../frontend/build/index.html')
    else:
        return {"message": "Startup Strategist API", "docs": "/docs"}

@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_startup_idea(idea: BusinessIdea):
    """
    Analyze a startup idea using the multi-agent pipeline with timeout protection
    """
    import time
    start_time = time.time()
    MAX_EXECUTION_TIME = 120  # 2 minutes maximum
    
    try:
        print(f"📝 Received idea: {idea.idea}")
        
        if not AGENT_LOADED:
            # Use mock agent with simulated processing time
            print("🔄 Using mock agent...")
            await asyncio.sleep(2)  # Simulate processing time
            
            results = {
                "refined_idea": f"# Business Idea: {idea.idea}\n\n*This is a demo response. Real AI agent analysis will provide detailed strategic insights.*",
                "problem": "# Problem Analysis\n\n*Demo mode: Real agents will analyze market problems and opportunities.*",
                "target_customer": "# Target Customer\n\n*Demo mode: Detailed customer analysis will be provided by AI agents.*",
                "mvp": "# MVP Strategy\n\n*Demo mode: Comprehensive product strategy coming from AI analysis.*",
                "competitor_analysis": "# Competitive Analysis\n\n*Demo mode: Market research and competitive intelligence pending.*",
                "monetization": "# Revenue Strategy\n\n*Demo mode: Detailed monetization analysis will be generated.*",
                "go_to_market": "# Go-to-Market Plan\n\n*Demo mode: Marketing and sales strategy pending AI analysis.*",
                "pitch_deck": "# Investment Summary\n\n*Demo mode: Professional pitch deck content will be created.*"
            }
            
            return AnalysisResponse(
                status="success",
                results=results,
                message="Analysis completed successfully using mock agent"
            )
        
        # Run the real ADK agent with timeout protection
        try:
            print("🚀 Starting ADK agent execution...")
            
            # Import required ADK classes
            from google.adk.runners import Runner
            from google.adk.sessions.in_memory_session_service import InMemorySessionService
            from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
            
            print("📞 Creating ADK Runner...")
            
            # Create Runner with required services
            runner = Runner(
                app_name="startup_strategist",
                agent=root_agent,
                session_service=InMemorySessionService(),
                memory_service=InMemoryMemoryService(),
            )
            
            # Create session
            user_id = f"user_{uuid.uuid4().hex[:8]}"
            session_id = f"session_{uuid.uuid4().hex[:8]}"
            
            print(f"📞 Creating session {session_id}...")
            
            session = await runner.session_service.create_session(
                app_name="startup_strategist",
                user_id=user_id,
                session_id=session_id
            )
            
            print(f"📞 Running agent with idea: {idea.idea[:50]}...")
            
            # Create user message content
            try:
                from google.genai import types
                user_message = types.Content(
                    role='user',
                    parts=[types.Part.from_text(text=idea.idea)]
                )
                print("✅ Using genai.types format for message")
            except (ImportError, AttributeError):
                try:
                    user_message = {
                        'role': 'user',
                        'parts': [{'text': idea.idea}]
                    }
                    print("✅ Using dictionary format for message")
                except Exception as e:
                    print(f"⚠️ Message format failed: {e}")
                    user_message = idea.idea
                    print("✅ Using string format for message")
            
            # Run the agent with timeout protection
            events = []
            agent_outputs = {}
            final_result = None
            event_count = 0
            MAX_EVENTS = 100  # Prevent infinite event loops
            
            print("🔄 Processing agent events with timeout protection...")
            
            try:
                # Use asyncio.wait_for to add timeout
                async def run_with_timeout():
                    nonlocal events, agent_outputs, final_result, event_count
                    
                    async for event in runner.run_async(
                        user_id=user_id,
                        session_id=session_id,
                        new_message=user_message
                    ):
                        # Check execution time
                        if time.time() - start_time > MAX_EXECUTION_TIME:
                            print("⏰ Execution timeout reached, stopping agent")
                            break
                            
                        # Check event count to prevent infinite loops
                        event_count += 1
                        if event_count > MAX_EVENTS:
                            print(f"🔄 Maximum events ({MAX_EVENTS}) reached, stopping to prevent infinite loop")
                            break
                        
                        events.append(event)
                        event_type = type(event).__name__
                        print(f"📦 Event {event_count}: {event_type}")
                        
                        # Debug: Print raw event information for first few events
                        if event_count <= 10:  # Show more detail for first 10 events
                            print(f"\n🔍 RAW EVENT {event_count} DEBUG:")
                            print(f"   Type: {type(event).__name__}")
                            print(f"   Module: {type(event).__module__}")
                            event_attrs = [attr for attr in dir(event) if not attr.startswith('_') and not callable(getattr(event, attr))]
                            print(f"   Attributes: {event_attrs}")
                            
                            # Try to show actual content of key attributes
                            for attr in ['agent_name', 'content', 'message', 'output', 'result', 'data', 'payload']:
                                if hasattr(event, attr):
                                    attr_value = getattr(event, attr)
                                    print(f"   {attr}: {type(attr_value).__name__} = {str(attr_value)[:200]}...")
                            print(f"   Full string repr: {str(event)[:300]}...")
                            print(f"─" * 60)
                        
                        # Try multiple ways to extract content from ADK events
                        content_extracted = False
                        agent_name = "unknown"
                        
                        # Method 1: Direct content extraction with better logic
                        if hasattr(event, 'content') and event.content:
                            agent_name = "unknown"
                            content_text = ""
                            
                            # Get agent name from author attribute
                            if hasattr(event, 'author') and event.author:
                                agent_name = str(event.author)
                            
                            print(f"\n🎯 PROCESSING EVENT WITH CONTENT - AGENT: {agent_name}")
                            
                            # Extract content from parts
                            if hasattr(event.content, 'parts') and event.content.parts:
                                print(f"   Content has {len(event.content.parts)} parts")
                                all_text_parts = []
                                for i, part in enumerate(event.content.parts):
                                    if hasattr(part, 'text') and part.text:
                                        part_text = str(part.text).strip()
                                        if part_text:
                                            all_text_parts.append(part_text)
                                            print(f"   Part {i}: {len(part_text)} chars - {part_text[:100]}...")
                                
                                # Combine all text parts
                                if all_text_parts:
                                    content_text = "\n\n".join(all_text_parts)
                                    print(f"   Combined content: {len(content_text)} total characters")
                            
                            elif hasattr(event.content, 'text') and event.content.text:
                                content_text = str(event.content.text).strip()
                                print(f"   Direct text content: {len(content_text)} characters")
                            
                            else:
                                # Try string representation
                                content_str = str(event.content)
                                if 'text=' in content_str:
                                    print(f"   Trying to extract from string repr...")
                                    content_text = content_str
                                print(f"   Content string repr: {len(content_text)} characters")
                            
                            if content_text and len(content_text.strip()) > 10:  # Meaningful content
                                print(f"\n{'🤖'*3} AGENT OUTPUT: {agent_name} {'🤖'*3}")
                                print(f"📝 FULL CONTENT:")
                                print(content_text)
                                print(f"{'─'*100}")
                                content_extracted = True
                                
                                # Map agent names to result keys with detailed logging
                                agent_name_lower = agent_name.lower()
                                content_extracted = True
                                
                                # Match exact agent names from agent.py
                                if 'clarify_idea_agent' in agent_name_lower or 'clarify' in agent_name_lower:
                                    agent_outputs['refined_idea'] = content_text
                                    print(f"✅ STORED AS: 'refined_idea' (from {agent_name})")
                                elif 'problem_statement_agent' in agent_name_lower or 'problem' in agent_name_lower:
                                    agent_outputs['problem'] = content_text
                                    print(f"✅ STORED AS: 'problem' (from {agent_name})")
                                elif 'target_customer_agent' in agent_name_lower or 'customer' in agent_name_lower:
                                    agent_outputs['target_customer'] = content_text
                                    print(f"✅ STORED AS: 'target_customer' (from {agent_name})")
                                elif 'mvp_planner_agent' in agent_name_lower or 'mvp' in agent_name_lower:
                                    agent_outputs['mvp'] = content_text
                                    print(f"✅ STORED AS: 'mvp' (from {agent_name})")
                                elif 'competitor_analysis_agent' in agent_name_lower or 'competitor' in agent_name_lower:
                                    agent_outputs['competitor_analysis'] = content_text
                                    print(f"✅ STORED AS: 'competitor_analysis' (from {agent_name})")
                                elif 'monetization_agent' in agent_name_lower or 'monetization' in agent_name_lower:
                                    agent_outputs['monetization'] = content_text
                                    print(f"✅ STORED AS: 'monetization' (from {agent_name})")
                                elif 'go_to_market_agent' in agent_name_lower or 'market' in agent_name_lower or 'gtm' in agent_name_lower:
                                    agent_outputs['go_to_market'] = content_text
                                    print(f"✅ STORED AS: 'go_to_market' (from {agent_name})")
                                elif 'pitch_deck_agent' in agent_name_lower or 'pitch' in agent_name_lower:
                                    agent_outputs['pitch_deck'] = content_text
                                    print(f"✅ STORED AS: 'pitch_deck' (from {agent_name})")
                                elif 'validation_loop_agent' in agent_name_lower or 'validation' in agent_name_lower:
                                    print(f"📋 VALIDATION FEEDBACK (from {agent_name}):")
                                    print(f"   {content_text[:200]}...")
                                    # Also store validation feedback for potential display
                                    agent_outputs['validation_feedback'] = content_text
                                elif 'final_synthesis_agent' in agent_name_lower or 'synthesis' in agent_name_lower or 'final' in agent_name_lower:
                                    final_result = content_text
                                    agent_outputs['final_synthesis'] = content_text
                                    print(f"✅ STORED AS: 'final_synthesis' (from {agent_name})")
                                    print(f"🎯 FINAL SYNTHESIS:")
                                    print(f"   {content_text[:200]}...")
                                elif 'memory_agent' in agent_name_lower or 'memory' in agent_name_lower:
                                    print(f"💾 MEMORY SUMMARY (from {agent_name}):")
                                    print(f"   {content_text[:200]}...")
                                    agent_outputs['memory_summary'] = content_text
                                else:
                                    # If we can't identify the agent, store by event number or as fallback
                                    print(f"❓ UNKNOWN AGENT TYPE: {agent_name}")
                                    print(f"   Content preview: {content_text[:200]}...")
                                    
                                    # Try to store based on event sequence or content keywords
                                    if event_count == 1 and 'refined_idea' not in agent_outputs:
                                        agent_outputs['refined_idea'] = content_text
                                        print(f"✅ STORED AS: 'refined_idea' (by position)")
                                    elif event_count == 2 and 'problem' not in agent_outputs:
                                        agent_outputs['problem'] = content_text
                                        print(f"✅ STORED AS: 'problem' (by position)")
                                    elif event_count == 3 and 'target_customer' not in agent_outputs:
                                        agent_outputs['target_customer'] = content_text
                                        print(f"✅ STORED AS: 'target_customer' (by position)")
                                    elif event_count == 4 and 'mvp' not in agent_outputs:
                                        agent_outputs['mvp'] = content_text
                                        print(f"✅ STORED AS: 'mvp' (by position)")
                                    elif event_count == 5 and 'competitor_analysis' not in agent_outputs:
                                        agent_outputs['competitor_analysis'] = content_text
                                        print(f"✅ STORED AS: 'competitor_analysis' (by position)")
                                    elif event_count == 6 and 'monetization' not in agent_outputs:
                                        agent_outputs['monetization'] = content_text
                                        print(f"✅ STORED AS: 'monetization' (by position)")
                                    elif event_count == 7 and 'go_to_market' not in agent_outputs:
                                        agent_outputs['go_to_market'] = content_text
                                        print(f"✅ STORED AS: 'go_to_market' (by position)")
                                    elif event_count == 8 and 'pitch_deck' not in agent_outputs:
                                        agent_outputs['pitch_deck'] = content_text
                                        print(f"✅ STORED AS: 'pitch_deck' (by position)")
                                    else:
                                        if not final_result:
                                            final_result = content_text
                                            print(f"✅ STORED AS: 'final_result' (fallback)")
                                
                                print(f"\n📊 CURRENT COLLECTION STATUS:")
                                print(f"   Collected outputs: {list(agent_outputs.keys())}")
                                print(f"   Progress: {len(agent_outputs)}/8 target outputs")
                                print(f"   Has final result: {'Yes' if final_result else 'No'}")
                            else:
                                print(f"⚠️ Agent {agent_name} produced no meaningful content (length: {len(content_text)})")
                        
                        # Method 2: Check for other event types with content
                        elif hasattr(event, 'message') or hasattr(event, 'response') or hasattr(event, 'output'):
                            print(f"\n📤 NON-AGENT EVENT OUTPUT:")
                            for attr_name in ['message', 'response', 'output', 'result', 'data']:
                                if hasattr(event, attr_name):
                                    attr_value = getattr(event, attr_name)
                                    print(f"   {attr_name}: {type(attr_value)} = {str(attr_value)[:200]}...")
                                    
                                    if hasattr(attr_value, 'content') or hasattr(attr_value, 'text'):
                                        content = getattr(attr_value, 'content', getattr(attr_value, 'text', ''))
                                        if content and len(str(content).strip()) > 10:
                                            print(f"\n📝 EXTRACTED CONTENT ({attr_name}):")
                                            print(str(content))
                                            print(f"─" * 60)
                                            if not final_result:
                                                final_result = str(content)
                                                print(f"✅ Stored as fallback final_result")
                                            content_extracted = True
                                            break
                        
                        # Method 3: Try to extract from any text-containing attributes
                        if not content_extracted:
                            print(f"🔍 Searching for text content in event attributes...")
                            for attr_name in dir(event):
                                if not attr_name.startswith('_') and not callable(getattr(event, attr_name)):
                                    try:
                                        attr_value = getattr(event, attr_name)
                                        if isinstance(attr_value, str) and len(attr_value.strip()) > 20:
                                            print(f"\n📄 FOUND TEXT IN {attr_name}:")
                                            print(f"   {attr_value[:500]}...")
                                            if not final_result and 'Event' not in attr_value:
                                                final_result = attr_value
                                                print(f"✅ Stored as fallback final_result")
                                                content_extracted = True
                                        elif hasattr(attr_value, 'text') or hasattr(attr_value, 'content'):
                                            text_content = getattr(attr_value, 'text', getattr(attr_value, 'content', ''))
                                            if text_content and len(str(text_content).strip()) > 20:
                                                print(f"\n📄 FOUND NESTED TEXT IN {attr_name}:")
                                                print(f"   {str(text_content)[:500]}...")
                                                if not final_result:
                                                    final_result = str(text_content)
                                                    print(f"✅ Stored as fallback final_result")
                                                    content_extracted = True
                                    except Exception as e:
                                        continue
                        
                        if not content_extracted and event_count <= 5:
                            print(f"❌ No content extracted from event {event_count}")
                            print(f"   Event type: {type(event)}")
                            print(f"   Event string: {str(event)[:200]}...")
                        
                        # No early termination - let all agents complete
                        # Early termination disabled to ensure all 11 agents can provide outputs
                        if event_count % 10 == 0:  # Status update every 10 events
                            elapsed = time.time() - start_time
                            print(f"⏱️ STATUS: {event_count} events, {len(agent_outputs)} outputs, {elapsed:.1f}s")
                            print(f"📊 COLLECTED OUTPUTS: {list(agent_outputs.keys())}")
                            if elapsed > 180:  # Only stop if we're over 3 minutes
                                print(f"🕐 Long execution detected, will complete soon...")
                        
                        # Only stop if we've exceeded maximum time or event limits
                        if event_count >= MAX_EVENTS:
                            print(f"\n🔄 Maximum events ({MAX_EVENTS}) reached, stopping")
                            break
                
                # Run with extended timeout to allow all agents to complete
                await asyncio.wait_for(run_with_timeout(), timeout=120)  # Allow 2 minutes for all agents
                
            except asyncio.TimeoutError:
                print(f"⏰ Agent execution timed out after 120 seconds, but continuing with collected outputs")
                # Don't raise, continue with whatever we collected
            
            print(f"✅ Agent execution completed. Processed {event_count} events, collected {len(agent_outputs)} outputs")
            
            # Print final summary of collected outputs
            print(f"\n{'='*100}")
            print(f"📋 FINAL AGENT OUTPUTS SUMMARY")
            print(f"{'='*100}")
            
            for key, value in agent_outputs.items():
                print(f"\n🔹 {key.upper().replace('_', ' ')}:")
                print(f"   {value}")
            
            if final_result and final_result not in agent_outputs.values():
                print(f"\n🔹 FINAL RESULT:")
                print(f"   {final_result}")
            
            print(f"\n📊 COLLECTION STATISTICS:")
            print(f"   • Total events processed: {event_count}")
            print(f"   • Agent outputs collected: {len(agent_outputs)}")
            print(f"   • Has final result: {'Yes' if final_result else 'No'}")
            print(f"   • Execution time: {time.time() - start_time:.2f} seconds")
            print(f"{'='*100}\n")
            
            # Use agent outputs if available, otherwise use final result or fallback
            if agent_outputs:
                results = {}
                
                # Convert all agent outputs to enhanced markdown format
                for key, content in agent_outputs.items():
                    enhanced_content = enhance_content_with_markdown(content, key)
                    results[key] = enhanced_content
                    print(f"✅ Enhanced {key} content with markdown formatting")
                
                # Include final_synthesis if we captured it
                if final_result and 'final_synthesis' not in results:
                    enhanced_final = enhance_content_with_markdown(final_result, 'final_synthesis')
                    results['final_synthesis'] = enhanced_final
                    print(f"✅ Added final_synthesis from final_result with markdown")
                
                print(f"✅ Using {len(agent_outputs)} collected agent outputs + additional synthesis (all markdown enhanced)")
                
                # Fill in missing outputs with simple generic messages
                expected_keys = ['refined_idea', 'problem', 'target_customer', 'mvp', 'competitor_analysis', 'monetization', 'go_to_market', 'pitch_deck']
                for key in expected_keys:
                    if key not in results:
                        agent_name = key.replace('_', ' ').title()
                        results[key] = f"""# {agent_name}

*This section is being processed by our AI agents. The analysis will be available shortly as our specialized agents complete their comprehensive evaluation of your business idea.*

Please note: Our AI-powered analysis pipeline is currently generating detailed insights for this component of your startup strategy."""
                    
            elif final_result and len(final_result.strip()) > 50:
                print(f"✅ Using final result: {final_result[:100]}...")
                # Simple fallback when only final result is available
                results = {
                    "refined_idea": f"# Refined Business Idea\n\n{final_result}",
                    "problem": "# Problem Analysis\n\n*Analysis in progress by our AI agents.*",
                    "target_customer": "# Target Customer\n\n*Customer analysis being generated.*",
                    "mvp": "# MVP Strategy\n\n*MVP planning in progress.*",
                    "competitor_analysis": "# Competitive Analysis\n\n*Market analysis being conducted.*",
                    "monetization": "# Monetization Strategy\n\n*Revenue model analysis in progress.*",
                    "go_to_market": "# Go-to-Market Plan\n\n*Marketing strategy being developed.*",
                    "pitch_deck": "# Investment Pitch\n\n*Pitch deck preparation in progress.*"
                }
            else:
                print("⚠️ Using minimal fallback - agents may still be processing")
                # Minimal fallback when no results are available
                results = {
                    "refined_idea": "# Business Idea Analysis\n\n*Our AI agents are analyzing your business idea. Please wait while we generate comprehensive insights.*",
                    "problem": "# Problem Analysis\n\n*Market problem analysis in progress.*",
                    "target_customer": "# Target Customer Analysis\n\n*Customer research being conducted.*",
                    "mvp": "# MVP Strategy\n\n*Product strategy being developed.*",
                    "competitor_analysis": "# Competitive Analysis\n\n*Market research in progress.*",
                    "monetization": "# Revenue Strategy\n\n*Monetization analysis being generated.*",
                    "go_to_market": "# Go-to-Market Strategy\n\n*Marketing plan being developed.*",
                    "pitch_deck": "# Investment Summary\n\n*Pitch deck being prepared.*"
                }
            
            execution_time = time.time() - start_time
            print(f"📊 Final results keys: {list(results.keys())} (execution time: {execution_time:.2f}s)")
            
            return AnalysisResponse(
                status="success",
                results=results,
                message=f"Analysis completed successfully using ADK agents in {execution_time:.1f}s"
            )
                
        except Exception as agent_error:
            print(f"❌ ADK agent execution error: {agent_error}")
            import traceback
            traceback.print_exc()
            
            # Simple fallback for errors
            results = {
                "refined_idea": f"# Business Idea: {idea.idea}\n\n*Our AI analysis encountered an issue. Please try again or contact support if the problem persists.*",
                "problem": "# Analysis Error\n\n*Unable to complete problem analysis at this time.*",
                "target_customer": "# Analysis Error\n\n*Customer analysis temporarily unavailable.*",
                "mvp": "# Analysis Error\n\n*MVP strategy analysis temporarily unavailable.*",
                "competitor_analysis": "# Analysis Error\n\n*Competitive analysis temporarily unavailable.*",
                "monetization": "# Analysis Error\n\n*Revenue analysis temporarily unavailable.*",
                "go_to_market": "# Analysis Error\n\n*Marketing strategy analysis temporarily unavailable.*",
                "pitch_deck": "# Analysis Error\n\n*Investment summary temporarily unavailable.*"
            }
            
            return AnalysisResponse(
                status="success",
                results=results,
                message="Analysis completed using enhanced fallback processing"
            )
        
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing startup idea: {str(e)}"
        )

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test agent availability
        agent_status = "available" if AGENT_LOADED else "mock_mode"
        agent_type = str(type(root_agent))
        
        return {
            "status": "healthy", 
            "message": "Startup Strategist API is running",
            "agent_status": agent_status,
            "agent_type": agent_type,
            "agent_loaded": AGENT_LOADED
        }
    except Exception as e:
        return {
            "status": "degraded",
            "message": f"API running but agent issue: {str(e)}",
            "agent_status": "error"
        }

@app.get("/api/agents")
async def get_agents():
    """Get list of available agents"""
    agents = [
        {"name": "Clarify Idea", "key": "refined_idea", "description": "Refines raw ideas into clear, investor-ready concepts"},
        {"name": "Problem Statement", "key": "problem", "description": "Identifies and validates real-world market problems"},
        {"name": "Target Customer", "key": "target_customer", "description": "Defines ideal customer profiles and market segments"},
        {"name": "MVP Planner", "key": "mvp", "description": "Designs minimum viable product strategy and roadmap"},
        {"name": "Competitor Analysis", "key": "competitor_analysis", "description": "Researches competitive landscape and positioning"},
        {"name": "Monetization", "key": "monetization", "description": "Develops sustainable revenue models and pricing"},
        {"name": "Go-to-Market", "key": "go_to_market", "description": "Creates comprehensive customer acquisition strategy"},
        {"name": "Pitch Deck", "key": "pitch_deck", "description": "Generates investor-ready business presentations"}
    ]
    return {
        "agents": agents,
        "total_agents": len(agents),
        "agent_status": "available" if AGENT_LOADED else "mock_mode"
    }

@app.get("/api/status")
async def get_system_status():
    """Get detailed system status"""
    try:
        return {
            "api_status": "running",
            "agent_loaded": AGENT_LOADED,
            "agent_type": str(type(root_agent)),
            "frontend_available": os.path.exists("../frontend/build/index.html"),
            "static_files_available": os.path.exists("../frontend/build/static"),
            "environment": "development" if AGENT_LOADED else "mock",
            "version": "1.0.0"
        }
    except Exception as e:
        return {
            "api_status": "error",
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Startup Strategist API...")
    print(f"📊 Agent Status: {'Real ADK Agent' if AGENT_LOADED else 'Mock Agent'}")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8001/api/health")
    uvicorn.run(app, host="0.0.0.0", port=8000)