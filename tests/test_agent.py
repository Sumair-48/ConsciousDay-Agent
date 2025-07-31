import unittest
from unittest.mock import patch, MagicMock
from agent.langchain_agent import ConsciousDayAgent

class TestConsciousDayAgent(unittest.TestCase):
    def setUp(self):
        """Set up test agent."""
        self.agent = ConsciousDayAgent()
    
    def test_agent_initialization(self):
        """Test agent initialization."""
        self.assertIsNotNone(self.agent)
    
    @patch('agent.langchain_agent.requests.post')
    def test_generate_reflection_success(self, mock_post):
        """Test successful reflection generation."""
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": """## Inner Reflection Summary
Test reflection content

## Dream Interpretation Summary
Test dream interpretation

## Energy/Mindset Insight
Test mindset insight

## Suggested Day Strategy
Test strategy content"""
                }
            }]
        }
        mock_post.return_value = mock_response
        
        # Test reflection generation
        result = self.agent.generate_reflection(
            journal="Test journal",
            intention="Test intention",
            dream="Test dream",
            priorities="Test priorities"
        )
        
        self.assertIsInstance(result, dict)
        self.assertIn('reflection', result)
        self.assertIn('strategy', result)
        self.assertIn('full_response', result)
    
    @patch('agent.langchain_agent.requests.post')
    def test_generate_reflection_api_failure(self, mock_post):
        """Test reflection generation with API failure."""
        # Mock API failure
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_post.return_value = mock_response
        
        # Test reflection generation
        result = self.agent.generate_reflection(
            journal="Test journal",
            intention="Test intention",
            dream="Test dream",
            priorities="Test priorities"
        )
        
        # Should return fallback response
        self.assertIsInstance(result, dict)
        self.assertIn('reflection', result)
        self.assertIn('strategy', result)
    
    def test_parse_response(self):
        """Test response parsing."""
        test_response = """## Inner Reflection Summary
This is a test reflection.

The reflection continues here.

## Dream Interpretation Summary
This is a test dream interpretation.

## Energy/Mindset Insight
This is a test mindset insight.

## Suggested Day Strategy
This is a test strategy.
With multiple lines."""
        
        sections = self.agent._parse_response(test_response)
        
        self.assertIn('reflection', sections)
        self.assertIn('dream_interpretation', sections)
        self.assertIn('mindset_insight', sections)
        self.assertIn('strategy', sections)
        
        self.assertIn('This is a test reflection', sections['reflection'])
        self.assertIn('This is a test dream interpretation', sections['dream_interpretation'])

if __name__ == '__main__':
    unittest.main()