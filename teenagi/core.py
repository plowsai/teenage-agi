"""
Core functionality for the TeenAGI package.
"""

import os
from typing import List, Optional, Union, Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

try:
    import openai
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import anthropic
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


class TeenAGI:
    """
    Main class for TeenAGI functionality.
    TeenAGI is an agent that can perform multiple function calls in sequence.
    """
    
    def __init__(self, name="TeenAGI", provider: str = "openai", model: Optional[str] = None):
        """
        Initialize a TeenAGI instance.
        
        Args:
            name (str): Name of the agent
            provider (str): "openai" or "anthropic"
            model (str, optional): Model to use (defaults to appropriate model for provider)
        """
        self.name = name
        self.capabilities = []
        self.provider = provider.lower()
        self.model = model
        self.client = None
        
        # Initialize provider client
        self._initialize_client()

    def _initialize_client(self):
        """Initialize the appropriate client based on the provider."""
        if self.provider == "openai":
            if not OPENAI_AVAILABLE:
                raise ImportError("OpenAI package is not installed. Install with 'pip install openai'")
            
            # Get API key from environment
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                raise ValueError(
                    "OpenAI API key not found. Please create a .env file with OPENAI_API_KEY=your_key"
                )
            
            self.client = OpenAI(api_key=api_key)
            self.model = self.model or "gpt-3.5-turbo"
            
        elif self.provider == "anthropic":
            if not ANTHROPIC_AVAILABLE:
                raise ImportError("Anthropic package is not installed. Install with 'pip install anthropic'")
            
            # Get API key from environment
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError(
                    "Anthropic API key not found. Please create a .env file with ANTHROPIC_API_KEY=your_key"
                )
            
            self.client = Anthropic(api_key=api_key)
            self.model = self.model or "claude-3-haiku-20240307"
        
        else:
            raise ValueError(f"Unsupported provider: {self.provider}. Use 'openai' or 'anthropic'")
    
    def learn(self, capability: str) -> bool:
        """
        Add a capability to the agent.
        
        Args:
            capability (str): A capability the agent should have
        
        Returns:
            bool: True if capability was successfully added
        """
        if not capability:
            return False
        
        self.capabilities.append(capability)
        return True
    
    def respond(self, prompt: str) -> str:
        """
        Generate a response that may involve multiple function calls.
        
        Args:
            prompt (str): Input prompt or task description
            
        Returns:
            str: Generated response
        """
        if not self.capabilities:
            return f"I'm {self.name}, but I don't have any capabilities yet."
        
        # Construct the prompt for the AI model
        system_message = self._construct_system_message()
        user_message = f"Task: {prompt}\n\nGenerate a helpful response using the capabilities I have."
        
        # Call the appropriate API based on provider
        return self._generate_response(system_message, user_message)
    
    def _construct_system_message(self) -> str:
        """Construct a system message based on agent capabilities."""
        capabilities_text = "\n".join([f"- {cap}" for cap in self.capabilities])
        return f"""You are {self.name}, an AI assistant with the following capabilities:

{capabilities_text}

When responding to user requests, you should determine which capabilities to use and in what sequence.
Explain your approach to solving the task by mentioning which capabilities you'll use.
"""

    def _generate_response(self, system_message: str, user_message: str) -> str:
        """Generate a response using the configured AI provider."""
        if self.provider == "openai":
            return self._generate_with_openai(system_message, user_message)
        elif self.provider == "anthropic":
            return self._generate_with_anthropic(system_message, user_message)
        else:
            # Fallback to basic response if no provider is configured
            capabilities_text = ", ".join(self.capabilities)
            return f"I'm {self.name}. For this request, I would use these capabilities: {capabilities_text}"
    
    def _generate_with_openai(self, system_message: str, user_message: str) -> str:
        """Generate a response using OpenAI API."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating response with OpenAI: {str(e)}"
    
    def _generate_with_anthropic(self, system_message: str, user_message: str) -> str:
        """Generate a response using Anthropic API."""
        try:
            prompt = f"{anthropic.HUMAN_PROMPT} {user_message} {anthropic.AI_PROMPT}"
            response = self.client.messages.create(
                model=self.model,
                system=system_message,
                messages=[{"role": "user", "content": user_message}],
                temperature=0.7,
                max_tokens=1000
            )
            return response.content[0].text
        except Exception as e:
            return f"Error generating response with Anthropic: {str(e)}"


def create_agent(name="TeenAGI", provider="openai", model=None):
    """
    Factory function to create a TeenAGI instance.
    
    Args:
        name (str): Name of the agent
        provider (str): "openai" or "anthropic"
        model (str, optional): Model to use
        
    Returns:
        TeenAGI: An initialized TeenAGI instance
    """
    return TeenAGI(name=name, provider=provider, model=model) 