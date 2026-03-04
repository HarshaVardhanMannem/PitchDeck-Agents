import React, { useState, useRef, useEffect } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
import { FiSend, FiUser, FiLoader, FiCheckCircle, FiClock } from 'react-icons/fi';
import { RiRobotLine } from 'react-icons/ri';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import './App.css';

const Container = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
`;

const ChatContainer = styled.div`
  width: 100%;
  max-width: 900px;
  height: 90vh;
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
`;

const Header = styled.div`
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  color: white;
  padding: 20px;
  text-align: center;
`;

const Title = styled.h1`
  margin: 0 0 8px 0;
  font-size: 24px;
  font-weight: 600;
`;

const Subtitle = styled.p`
  margin: 0;
  opacity: 0.9;
  font-size: 14px;
`;

const ChatArea = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #f8fafc;
`;

const MessageContainer = styled(motion.div)`
  margin-bottom: 20px;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  ${props => props.isUser && 'flex-direction: row-reverse;'}
`;

const Avatar = styled.div`
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: ${props => props.isUser ? '#4f46e5' : '#10b981'};
  color: white;
  flex-shrink: 0;
`;

const MessageBubble = styled.div`
  background: ${props => props.isUser ? '#4f46e5' : 'white'};
  color: ${props => props.isUser ? 'white' : '#374151'};
  padding: 12px 16px;
  border-radius: 18px;
  max-width: 70%;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  ${props => props.isUser && 'border-bottom-right-radius: 4px;'}
  ${props => !props.isUser && 'border-bottom-left-radius: 4px;'}
`;

const AgentProgress = styled.div`
  background: white;
  border-radius: 12px;
  padding: 16px;
  margin: 16px 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
`;

const AgentStep = styled.div`
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 0;
  border-bottom: ${props => props.isLast ? 'none' : '1px solid #e5e7eb'};
`;

const StepIcon = styled.div`
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: ${props => {
    if (props.status === 'completed') return '#10b981';
    if (props.status === 'in_progress') return '#f59e0b';
    return '#d1d5db';
  }};
  color: white;
`;

const StepText = styled.span`
  flex: 1;
  color: ${props => props.status === 'pending' ? '#9ca3af' : '#374151'};
  font-weight: ${props => props.status === 'in_progress' ? '600' : '400'};
`;

const InputContainer = styled.div`
  padding: 20px;
  background: white;
  border-top: 1px solid #e5e7eb;
`;

const InputWrapper = styled.div`
  display: flex;
  gap: 12px;
  align-items: center;
`;

const Input = styled.input`
  flex: 1;
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 25px;
  outline: none;
  font-size: 14px;
  transition: border-color 0.2s;

  &:focus {
    border-color: #4f46e5;
  }

  &:disabled {
    background: #f3f4f6;
    color: #9ca3af;
  }
`;

const SendButton = styled.button`
  width: 48px;
  height: 48px;
  border: none;
  border-radius: 50%;
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: transform 0.2s;

  &:hover:not(:disabled) {
    transform: scale(1.05);
  }

  &:disabled {
    background: #d1d5db;
    cursor: not-allowed;
    transform: none;
  }
`;

const ResultSection = styled.div`
  background: white;
  border-radius: 12px;
  padding: 24px;
  margin: 16px 0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-left: 4px solid #4f46e5;
  transition: transform 0.2s, box-shadow 0.2s;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
  }
`;

const ResultTitle = styled.h3`
  margin: 0 0 16px 0;
  color: #1f2937;
  font-size: 20px;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 12px;
`;

const AgentIcon = styled.span`
  font-size: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  border-radius: 12px;
  color: white;
  font-size: 18px;
`;

const ResultContent = styled.div`
  color: #374151;
  line-height: 1.7;
  font-size: 15px;
  
  /* Markdown styling */
  h1, h2, h3, h4, h5, h6 {
    color: #1f2937;
    margin: 16px 0 8px 0;
    font-weight: 600;
    
    &:first-child {
      margin-top: 0;
    }
  }
  
  h1 { font-size: 1.5em; }
  h2 { font-size: 1.3em; }
  h3 { font-size: 1.1em; }
  
  p {
    margin: 0 0 12px 0;
    
    &:last-child {
      margin-bottom: 0;
    }
  }
  
  /* Make the content more readable */
  strong, b {
    color: #1f2937;
    font-weight: 600;
  }
  
  em, i {
    font-style: italic;
    color: #4b5563;
  }
  
  /* Style bullet points */
  ul, ol {
    padding-left: 20px;
    margin: 12px 0;
  }
  
  li {
    margin-bottom: 6px;
    line-height: 1.6;
  }
  
  /* Code styling */
  code {
    background: #f3f4f6;
    padding: 2px 6px;
    border-radius: 4px;
    font-family: 'Monaco', 'Menlo', monospace;
    font-size: 0.9em;
    color: #dc2626;
  }
  
  pre {
    background: #f8fafc;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 16px;
    overflow-x: auto;
    margin: 12px 0;
    
    code {
      background: none;
      padding: 0;
      color: #374151;
    }
  }
  
  /* Blockquotes */
  blockquote {
    border-left: 4px solid #4f46e5;
    background: #f8fafc;
    margin: 12px 0;
    padding: 12px 16px;
    border-radius: 0 8px 8px 0;
    
    p {
      margin: 0;
      font-style: italic;
    }
  }
  
  /* Tables */
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    overflow: hidden;
  }
  
  th, td {
    padding: 8px 12px;
    text-align: left;
    border-bottom: 1px solid #e5e7eb;
  }
  
  th {
    background: #f8fafc;
    font-weight: 600;
    color: #1f2937;
  }
  
  tr:hover {
    background: #f9fafb;
  }
  
  /* Horizontal rules */
  hr {
    border: none;
    height: 1px;
    background: #e5e7eb;
    margin: 24px 0;
  }
  
  /* Links */
  a {
    color: #4f46e5;
    text-decoration: none;
    
    &:hover {
      text-decoration: underline;
    }
  }
`;

const agents = [
  { name: 'Clarify Idea', key: 'refined_idea', icon: '💡' },
  { name: 'Problem Statement', key: 'problem', icon: '🎯' },
  { name: 'Target Customer', key: 'target_customer', icon: '👥' },
  { name: 'MVP Planner', key: 'mvp', icon: '🛠️' },
  { name: 'Competitor Analysis', key: 'competitor_analysis', icon: '🏢' },
  { name: 'Monetization', key: 'monetization', icon: '💰' },
  { name: 'Go-to-Market', key: 'go_to_market', icon: '📈' },
  { name: 'Pitch Deck', key: 'pitch_deck', icon: '📊' },
  { name: 'Validation Feedback', key: 'validation_feedback', icon: '✅' },
  { name: 'Final Synthesis', key: 'final_synthesis', icon: '🎯' },
  { name: 'Memory Summary', key: 'memory_summary', icon: '💾' }
];

function App() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Hi! I'm your Startup Strategist AI. Share your business idea with me, and I'll help you transform it into a comprehensive startup strategy through my 8-agent analysis pipeline. What's your startup idea?",
      isUser: false,
      timestamp: new Date()
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [agentProgress, setAgentProgress] = useState([]);
  const [results, setResults] = useState({});
  const chatAreaRef = useRef(null);

  useEffect(() => {
    if (chatAreaRef.current) {
      chatAreaRef.current.scrollTop = chatAreaRef.current.scrollHeight;
    }
  }, [messages, agentProgress]);

  const sendMessage = async () => {
    if (!inputValue.trim() || isProcessing) return;

    const userMessage = {
      id: Date.now(),
      text: inputValue,
      isUser: true,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsProcessing(true);

    // Initialize agent progress
    const initialProgress = agents.map((agent, index) => ({
      ...agent,
      status: index === 0 ? 'in_progress' : 'pending'
    }));
    setAgentProgress(initialProgress);

    try {
      // Call the real backend API
      const response = await axios.post('http://localhost:8000/api/analyze', {
        idea: inputValue
      });

      console.log('Backend response:', response.data);
      console.log('Response status:', response.data.status);
      console.log('Response results:', response.data.results);
      console.log('Available result keys:', Object.keys(response.data.results || {}));

      // Check if we got successful results
      if (response.data.status === 'success' && response.data.results) {
        const backendResults = response.data.results;
        console.log('Processing backend results:', backendResults);
        
        // Immediately display all results we received
        const availableResults = Object.keys(backendResults);
        console.log('Available result keys from backend:', availableResults);
        
        // First, set all the results immediately
        setResults(backendResults);
        console.log('Set all results at once:', Object.keys(backendResults));
        
        // Update the progress indicators to show completion for agents that have results
        const updatedProgress = agents.map((agent, index) => {
          if (backendResults[agent.key]) {
            console.log(`✅ Agent ${agent.name} has result`);
            return { ...agent, status: 'completed' };
          } else {
            console.log(`❌ Agent ${agent.name} has no result`);
            return { ...agent, status: 'pending' };
          }
        });
        
        setAgentProgress(updatedProgress);
        
        // Show completion message
        const completedCount = availableResults.length;
        const botMessage = {
          id: Date.now() + 1,
          text: `✅ Analysis Complete! I've successfully analyzed your startup idea using ${completedCount} specialized agents. Each section below contains detailed insights to help you build a successful startup strategy. ${response.data.message || ''}`,
          isUser: false,
          timestamp: new Date()
        };

        setMessages(prev => [...prev, botMessage]);

      } else {
        // Handle error response
        console.error('Backend response not successful:', response.data);
        throw new Error(response.data.message || 'Analysis failed');
      }
    } catch (error) {
      console.error('Error:', error);
      
      // Reset agent progress on error
      setAgentProgress([]);
      
      let errorText = "I'm sorry, but I encountered an error processing your request. ";
      
      if (error.response) {
        // Backend returned an error response
        errorText += `Server error: ${error.response.data?.detail || error.response.statusText}`;
      } else if (error.request) {
        // Network error
        errorText += "Unable to connect to the server. Please make sure the backend is running on http://localhost:8000";
      } else {
        // Other error
        errorText += error.message;
      }
      
      const errorMessage = {
        id: Date.now() + 1,
        text: errorText,
        isUser: false,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  };

  return (
    <Container>
      <ChatContainer>
        <Header>
          <Title>🚀 Startup Strategist AI</Title>
          <Subtitle>Transform your business idea into an investor-ready strategy</Subtitle>
        </Header>

        <ChatArea ref={chatAreaRef}>
          <AnimatePresence>
            {messages.map((message) => (
              <MessageContainer
                key={message.id}
                isUser={message.isUser}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.3 }}
              >
                <Avatar isUser={message.isUser}>
                  {message.isUser ? <FiUser size={20} /> : <RiRobotLine size={20} />}
                </Avatar>
                <MessageBubble isUser={message.isUser}>
                  {message.text}
                </MessageBubble>
              </MessageContainer>
            ))}
          </AnimatePresence>

          {agentProgress.length > 0 && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
            >
              <AgentProgress>
                <h4 style={{ margin: '0 0 16px 0', color: '#1f2937' }}>
                  Analysis Progress
                </h4>
                {agentProgress.map((agent, index) => (
                  <AgentStep key={agent.key} isLast={index === agentProgress.length - 1}>
                    <StepIcon status={agent.status}>
                      {agent.status === 'completed' && <FiCheckCircle size={14} />}
                      {agent.status === 'in_progress' && <FiLoader size={14} />}
                      {agent.status === 'pending' && <FiClock size={14} />}
                    </StepIcon>
                    <StepText status={agent.status}>
                      {agent.name}
                      {agent.status === 'in_progress' && ' (Processing...)'}
                      {agent.status === 'completed' && ' ✓'}
                    </StepText>
                  </AgentStep>
                ))}
              </AgentProgress>
            </motion.div>
          )}

          {/* Results Counter */}
          {Object.keys(results).length > 0 && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              style={{ 
                background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)', 
                color: 'white',
                padding: '12px 16px', 
                margin: '10px 0', 
                borderRadius: '8px', 
                fontSize: '14px',
                fontWeight: '600',
                textAlign: 'center'
              }}
            >
              📋 {Object.keys(results).length} Agent Analysis Complete
            </motion.div>
          )}

          {Object.keys(results).map((key) => {
            const agent = agents.find(a => a.key === key);
            console.log(`Rendering result for key: ${key}, agent:`, agent);
            return (
              <motion.div
                key={key}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
              >
                <ResultSection>
                  <ResultTitle>
                    <AgentIcon>{agent?.icon || '🎯'}</AgentIcon>
                    <span>{agent?.name || key}</span>
                  </ResultTitle>
                  <ResultContent>
                    <ReactMarkdown 
                      remarkPlugins={[remarkGfm]}
                      components={{
                        // Customize rendering of specific elements if needed
                        h1: ({children, ...props}) => <h1 style={{color: '#1f2937', fontSize: '1.5em'}} {...props}>{children}</h1>,
                        h2: ({children, ...props}) => <h2 style={{color: '#1f2937', fontSize: '1.3em'}} {...props}>{children}</h2>,
                        h3: ({children, ...props}) => <h3 style={{color: '#1f2937', fontSize: '1.1em'}} {...props}>{children}</h3>,
                      }}
                    >
                      {results[key]}
                    </ReactMarkdown>
                  </ResultContent>
                </ResultSection>
              </motion.div>
            );
          })}
        </ChatArea>

        <InputContainer>
          <InputWrapper>
            <Input
              type="text"
              placeholder={isProcessing ? "Processing your idea..." : "Describe your startup idea..."}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={isProcessing}
            />
            <SendButton onClick={sendMessage} disabled={isProcessing || !inputValue.trim()}>
              {isProcessing ? <FiLoader size={20} /> : <FiSend size={20} />}
            </SendButton>
          </InputWrapper>
        </InputContainer>
      </ChatContainer>
    </Container>
  );
}

export default App;