import logging
from typing import Dict, Optional
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from agent.prompts import PROMPT_TEMPLATE, REFLECTION_SYSTEM_PROMPT
from config.settings import Config
import requests

class ConsciousDayAgent:
    def __init__(self):
        self.api_key = Config.OPENROUTER_API_KEY
        self.base_url = Config.OPENROUTER_BASE_URL
        self.model = Config.DEFAULT_MODEL
        
        if not self.api_key:
            logging.warning("No API key found. Agent will not function properly.")
    
    def _make_api_request(self, messages: list) -> str:
        """Make a direct API request to OpenRouter."""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://consciousday-agent.streamlit.app",
                "X-Title": "ConsciousDay Agent"
            }
            
            data = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 1500
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                logging.error(f"API request failed: {response.status_code} - {response.text}")
                return self._get_fallback_response()
                
        except Exception as e:
            logging.error(f"Error making API request: {e}")
            return self._get_fallback_response()
    
    def _get_fallback_response(self) -> str:
        """Provide a fallback response when API fails."""
        return """
## Inner Reflection Summary
I'm currently unable to process your journal entry due to a technical issue. However, taking time to write down your thoughts is already a valuable practice for self-reflection.

## Dream Interpretation Summary
Dreams often reflect our subconscious processing of daily experiences and emotions. Consider what themes or feelings stood out to you.

## Energy/Mindset Insight
Your intention and priorities show that you're actively working to create meaningful days. This self-awareness is a strength to build upon.

## Suggested Day Strategy
1. Start with your most important priority when your energy is highest
2. Take regular breaks to check in with yourself
3. Stay flexible and adjust your plan as needed
4. End the day with gratitude for what you accomplished

*Note: This is a simplified response due to technical limitations. Please try again later for a more personalized analysis.*
"""
    
    def generate_reflection(self, journal: str, intention: str, dream: str, priorities: str) -> Dict[str, str]:
        """Generate reflection and strategy based on user inputs."""
        try:
            # Format the prompt with user inputs
            formatted_prompt = PROMPT_TEMPLATE.format(
                journal=journal,
                intention=intention,
                dream=dream if dream else "No dream recalled",
                priorities=priorities
            )
            
            messages = [
                {"role": "system", "content": REFLECTION_SYSTEM_PROMPT},
                {"role": "user", "content": formatted_prompt}
            ]
            
            response = self._make_api_request(messages)
            
            # Parse the response into sections
            sections = self._parse_response(response)
            
            return {
                "reflection": sections.get("reflection", ""),
                "dream_interpretation": sections.get("dream_interpretation", ""),
                "mindset_insight": sections.get("mindset_insight", ""),
                "strategy": sections.get("strategy", ""),
                "full_response": response
            }
            
        except Exception as e:
            logging.error(f"Error generating reflection: {e}")
            fallback = self._get_fallback_response()
            return {
                "reflection": "Unable to generate reflection at this time.",
                "dream_interpretation": "Unable to interpret dream at this time.",
                "mindset_insight": "Unable to provide mindset insight at this time.",
                "strategy": "Please focus on your top priorities for today.",
                "full_response": fallback
            }
    
    def _parse_response(self, response: str) -> Dict[str, str]:
        """Parse the AI response into structured sections."""
        sections = {}
        current_section = None
        current_content = []
        
        lines = response.split('\n')
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('## Inner Reflection Summary'):
                current_section = 'reflection'
                current_content = []
            elif line.startswith('## Dream Interpretation Summary'):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'dream_interpretation'
                current_content = []
            elif line.startswith('## Energy/Mindset Insight'):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'mindset_insight'
                current_content = []
            elif line.startswith('## Suggested Day Strategy'):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'strategy'
                current_content = []
            elif current_section and line:
                current_content.append(line)
        
        # Add the last section
        if current_section and current_content:
            sections[current_section] = '\n'.join(current_content).strip()
        
        return sections