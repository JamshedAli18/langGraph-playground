"""
Tests for simple_agent.py

This module contains basic tests for the simple agent implementation.
"""

import unittest
from simple_agent import create_simple_agent, run_simple_agent, chatbot, AgentState


class TestSimpleAgent(unittest.TestCase):
    """Test cases for the simple agent."""
    
    def test_chatbot_function(self):
        """Test the chatbot function through the agent."""
        # Create the agent and run it
        app = create_simple_agent()
        result = app.invoke({"messages": [{"role": "user", "content": "Hello"}]})
        
        # Check that a response was generated
        self.assertIn("messages", result)
        self.assertGreaterEqual(len(result["messages"]), 2)
        # Last message should be the echo
        self.assertIn("Echo:", result["messages"][-1].content)
    
    def test_chatbot_with_empty_messages(self):
        """Test agent with empty state."""
        app = create_simple_agent()
        # Should handle empty messages gracefully
        result = app.invoke({"messages": []})
        
        # Should return empty messages
        self.assertEqual(len(result["messages"]), 0)
    
    def test_create_simple_agent(self):
        """Test agent creation."""
        app = create_simple_agent()
        
        # Check that the app was created
        self.assertIsNotNone(app)
    
    def test_run_simple_agent(self):
        """Test running the agent with user input."""
        response = run_simple_agent("Test message")
        
        # Check that we got a response
        self.assertIsNotNone(response)
        self.assertIn("Echo:", response)
        self.assertIn("Test message", response)
    
    def test_agent_with_multiple_messages(self):
        """Test the agent with different messages."""
        test_cases = [
            ("Hello!", "Echo: Hello!"),
            ("How are you?", "Echo: How are you?"),
            ("What's your name?", "Echo: What's your name?")
        ]
        
        for input_msg, expected_output in test_cases:
            response = run_simple_agent(input_msg)
            self.assertEqual(response, expected_output)


if __name__ == "__main__":
    unittest.main()
