#!/usr/bin/env python
"""
Demo script for TeenAGI's function calling capabilities.

Make sure to set your Anthropic API key in a .env file before running:
ANTHROPIC_API_KEY=your_key_here
"""

import os
import sys
import requests
import datetime
from typing import List, Dict, Any, Optional

# Add parent directory to path to import teenagi
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from teenagi import TeenAGI, configure_logger

# Configure logging to show DEBUG messages
configure_logger(level="DEBUG")

# Create an agent using Anthropic
agent = TeenAGI(
    name="ResearchAssistant",
    provider="anthropic",
    model="claude-3-haiku-20240307"  # You can change to a different Claude model
)

# Register some example functions
@agent.register_function(description="Get the current date and time")
def get_current_time() -> str:
    """Get the current date and time."""
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

@agent.register_function(description="Search for information on a topic")
def search_info(query: str) -> str:
    """
    Search for information on a given topic.
    
    Args:
        query: The search query
        
    Returns:
        Search results as text
    """
    # This is a mock implementation - in a real app, you'd use a search API
    return f"Here are the search results for '{query}':\n" + \
           f"1. {query} is a popular topic with many resources available.\n" + \
           f"2. The latest research on {query} shows promising results.\n" + \
           f"3. Experts in {query} recommend starting with basic concepts."

@agent.register_function(description="Get weather information for a location")
def get_weather(location: str) -> Dict[str, Any]:
    """
    Get current weather for a location.
    
    Args:
        location: City name or location
        
    Returns:
        Weather information
    """
    # Mock weather data - in a real app, you'd call a weather API
    weather_data = {
        "location": location,
        "temperature": 72,
        "condition": "Sunny",
        "humidity": 65,
        "wind_speed": 5
    }
    return weather_data

@agent.register_function(description="Calculate mathematical expression")
def calculate(expression: str) -> float:
    """
    Evaluate a mathematical expression.
    
    Args:
        expression: Mathematical expression as string
        
    Returns:
        Result of calculation
    """
    try:
        # Security note: eval is used for demo purposes only
        # In production code, use a safer alternative like ast.literal_eval
        # or a proper math expression parser
        result = eval(expression)
        return float(result)
    except Exception as e:
        return f"Error: {str(e)}"

# Define agent capabilities
agent.learn("can search for information online")
agent.learn("can perform calculations")
agent.learn("can get current weather information")
agent.learn("can get the current date and time")

# Test the agent with some prompts
def test_agent():
    prompts = [
        "What time is it right now?",
        "What's the weather like in San Francisco?",
        "Calculate 15 * 7 + 22 / 2",
        "Can you find information about machine learning?",
        "I need the current time and the weather in New York"
    ]
    
    for i, prompt in enumerate(prompts, 1):
        print(f"\n--- Test {i}: {prompt} ---")
        response = agent.respond(prompt)
        print(f"\nResponse:\n{response}")
        print("-" * 50)

if __name__ == "__main__":
    print("TeenAGI Function Calling Demo")
    print("=" * 50)
    test_agent() 