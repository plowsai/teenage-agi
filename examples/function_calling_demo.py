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
import json
from typing import List, Dict, Any, Optional

# Add parent directory to path to import teenagi
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from teenagi import TeenAGI, configure_logger

# Try to import duckduckgo_search for real search results
try:
    from duckduckgo_search import DDGS
    DDGS_AVAILABLE = True
except ImportError:
    DDGS_AVAILABLE = False

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
def search_info(query: str, num_results: int = 3) -> str:
    """
    Search for real information on a given topic using DuckDuckGo.
    
    Args:
        query: The search query
        num_results: Number of results to return (default: 3)
        
    Returns:
        Search results as text
    """
    if DDGS_AVAILABLE:
        try:
            # Use DuckDuckGo Search API
            ddgs = DDGS()
            results = list(ddgs.text(query, max_results=num_results))
            
            if not results:
                return f"No results found for '{query}'"
            
            # Format search results
            formatted_results = f"Search results for '{query}':\n\n"
            for i, result in enumerate(results, 1):
                formatted_results += f"{i}. {result['title']}\n"
                formatted_results += f"   {result['body']}\n"
                formatted_results += f"   Source: {result['href']}\n\n"
            
            return formatted_results
        except Exception as e:
            # Fallback to mock results if there's an error
            return f"Error searching for '{query}': {str(e)}\nFalling back to mock results."
    else:
        # Fallback for when duckduckgo-search is not installed
        return f"Real search is not available (duckduckgo-search not installed).\nMock results for '{query}':\n" + \
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
    try:
        # Try to use a real weather API (OpenWeatherMap)
        # You need to sign up for a free API key at https://openweathermap.org/
        api_key = os.environ.get("OPENWEATHER_API_KEY")
        
        if api_key:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=imperial"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                weather_data = {
                    "location": location,
                    "temperature": data["main"]["temp"],
                    "condition": data["weather"][0]["description"],
                    "humidity": data["main"]["humidity"],
                    "wind_speed": data["wind"]["speed"]
                }
                return weather_data
    except Exception as e:
        print(f"Error fetching weather data: {e}")
    
    # Mock weather data as fallback
    weather_data = {
        "location": location,
        "temperature": 72,
        "condition": "Sunny (mock data)",
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
        "Find information about machine learning and summarize it",
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
    
    # Check if required packages are installed
    if not DDGS_AVAILABLE:
        print("Note: duckduckgo-search package is not installed.")
        print("To enable real search, install it with: pip install duckduckgo-search")
    
    test_agent() 