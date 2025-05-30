"""
Core functionality for the TeenAGI package.
"""

import os
import json
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

from .function_registry import registry
from .logger import logger


class TeenAGI:
    """
    Main class for TeenAGI functionality.
    TeenAGI is an agent that can perform multiple function calls in sequence.
    """
    
    def __init__(self, name="TeenAGI", provider: str = "openai", model: Optional[str] = None,
                 log_level: str = "INFO", log_to_file: bool = False):
        """
        Initialize a TeenAGI instance.
        
        Args:
            name (str): Name of the agent
            provider (str): "openai" or "anthropic"
            model (str, optional): Model to use (defaults to appropriate model for provider)
            log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_to_file (bool): Whether to log to a file (teenagi.log)
        """
        self.name = name
        self.capabilities = []
        self.provider = provider.lower()
        self.model = model
        self.client = None
        self.function_registry = registry
        self.conversation_history = []
        
        # Set up logging
        logger.set_level(log_level)
        if log_to_file:
            logger.set_to_file = True
        
        logger.info(f"Initializing {self.name} with provider: {self.provider}")
        
        # Initialize provider client
        self._initialize_client()

    def _initialize_client(self):
        """Initialize the appropriate client based on the provider."""
        if self.provider == "openai":
            if not OPENAI_AVAILABLE:
                logger.error("OpenAI package is not installed")
                raise ImportError("OpenAI package is not installed. Install with 'pip install openai'")
            
            # Get API key from environment
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                logger.error("OpenAI API key not found in environment")
                raise ValueError(
                    "OpenAI API key not found. Please create a .env file with OPENAI_API_KEY=your_key"
                )
            
            self.client = OpenAI(api_key=api_key)
            self.model = self.model or "gpt-3.5-turbo"
            logger.info(f"Using OpenAI model: {self.model}")
            
        elif self.provider == "anthropic":
            if not ANTHROPIC_AVAILABLE:
                logger.error("Anthropic package is not installed")
                raise ImportError("Anthropic package is not installed. Install with 'pip install anthropic'")
            
            # Get API key from environment
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                logger.error("Anthropic API key not found in environment")
                raise ValueError(
                    "Anthropic API key not found. Please create a .env file with ANTHROPIC_API_KEY=your_key"
                )
            
            self.client = Anthropic(api_key=api_key)
            self.model = self.model or "claude-3-haiku-20240307"
            logger.info(f"Using Anthropic model: {self.model}")
        
        else:
            logger.error(f"Unsupported provider: {self.provider}")
            raise ValueError(f"Unsupported provider: {self.provider}. Use 'openai' or 'anthropic'")
    
    def register_function(self, func=None, *, name=None, description=None):
        """
        Register a function that can be called by the agent.
        
        Can be used as a decorator:
        
        @agent.register_function(description="Search the web for information")
        def search_web(query: str) -> str:
            ...
            
        Args:
            func: The function to register
            name: Optional custom name for the function
            description: Description of what the function does
            
        Returns:
            The original function (for decorator usage)
        """
        return self.function_registry.register(func, name=name, description=description)
    
    def learn(self, capability: str) -> bool:
        """
        Add a capability to the agent.
        
        Args:
            capability (str): A capability the agent should have
        
        Returns:
            bool: True if capability was successfully added
        """
        if not capability:
            logger.warning("Attempted to add empty capability")
            return False
        
        self.capabilities.append(capability)
        logger.info(f"Added capability: {capability}")
        return True
    
    def respond(self, prompt: str, max_function_calls: int = 3) -> str:
        """
        Generate a response that may involve multiple function calls.
        
        Args:
            prompt (str): Input prompt or task description
            max_function_calls (int): Maximum number of function calls to make
            
        Returns:
            str: Generated response
        """
        logger.info(f"Processing request: {prompt}")
        
        if not self.capabilities:
            logger.warning("No capabilities defined")
            return f"I'm {self.name}, but I don't have any capabilities yet."
        
        if not self.function_registry.functions:
            logger.info("No functions registered, using default response")
            return self._generate_default_response(prompt)
        
        # Start conversation with the prompt
        self.conversation_history = []
        user_message = prompt
        
        final_response = ""
        function_calls_made = 0
        
        # Loop for multiple function calls
        while function_calls_made < max_function_calls:
            # Construct the prompt for the AI model
            system_message = self._construct_system_message()
            
            # Get response from the model
            logger.debug(f"Sending request to {self.provider}")
            ai_response = self._generate_response(system_message, user_message)
            
            # Check if the response contains a function call
            function_call = self._extract_function_call(ai_response)
            
            if function_call:
                # Execute the function
                logger.info(f"Executing function: {function_call.get('name')}")
                function_result = self.function_registry.parse_and_execute(function_call)
                
                if function_result.get('error'):
                    logger.error(f"Function execution error: {function_result.get('error')}")
                    final_response = f"I encountered an error while executing the function: {function_result.get('error')}"
                    break
                
                # Add function call and result to conversation history
                self.conversation_history.append({
                    "role": "function",
                    "name": function_call.get('name'),
                    "content": str(function_result.get('result'))
                })
                
                # Update user message to include function result
                user_message = f"The function {function_call.get('name')} returned: {function_result.get('result')}\nPlease continue processing the original request."
                
                function_calls_made += 1
                logger.debug(f"Function call {function_calls_made}/{max_function_calls} completed")
                
            else:
                # No function call, this is the final response
                final_response = ai_response
                break
        
        if not final_response:
            # If we reached max function calls without a final response
            logger.warning(f"Reached max function calls ({max_function_calls}) without final response")
            final_response = self._generate_response(
                system_message,
                f"Please provide a final response based on the functions we've executed so far."
            )
        
        logger.info("Request processing completed")
        return final_response
    
    def _extract_function_call(self, response: str) -> Optional[Dict[str, Any]]:
        """
        Extract a function call from the LLM response.
        
        This is a heuristic method since different LLMs format function calls differently.
        Ideally, we would use the tool calling capabilities of the LLMs directly.
        
        Args:
            response: The response from the LLM
            
        Returns:
            Dictionary with function call details or None
        """
        # Look for function call patterns like:
        # function_name(arg1="value1", arg2="value2")
        # or JSON-like: {"name": "function_name", "arguments": {"arg1": "value1"}}
        
        # Try to find JSON-like patterns first
        try:
            # Try to extract JSON from the response
            import re
            json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
                function_data = json.loads(json_str)
                if 'name' in function_data:
                    return function_data
        except Exception as e:
            logger.debug(f"JSON extraction failed: {e}")
        
        # Try to find function call patterns
        for func_name in self.function_registry.functions.keys():
            # Look for patterns like: func_name(args) or func_name(arg1="value1", arg2="value2")
            import re
            pattern = fr'{func_name}\s*\((.*?)\)'
            match = re.search(pattern, response, re.DOTALL)
            
            if match:
                args_str = match.group(1)
                
                # Convert to JSON format
                try:
                    # Try to parse as Python code
                    # Not secure, but we're just trying to extract function arguments
                    # This won't work well for complex arguments
                    import ast
                    
                    # Add quotes to keys if missing
                    args_str = re.sub(r'(\w+)=', r'"\1"=', args_str)
                    # Replace = with :
                    args_str = args_str.replace('=', ':')
                    # Wrap in curly braces
                    args_dict_str = '{' + args_str + '}'
                    
                    # Try to parse as JSON
                    args_dict = json.loads(args_dict_str)
                    
                    return {
                        "name": func_name,
                        "arguments": json.dumps(args_dict)
                    }
                except Exception as e:
                    logger.debug(f"Function arg parsing failed: {e}")
                    # If parsing fails, still return a function call with empty args
                    return {
                        "name": func_name,
                        "arguments": "{}"
                    }
        
        return None
    
    def _construct_system_message(self) -> str:
        """Construct a system message based on agent capabilities and available functions."""
        capabilities_text = "\n".join([f"- {cap}" for cap in self.capabilities])
        
        # Get descriptions of available functions
        function_descriptions = self.function_registry.get_function_descriptions()
        functions_text = ""
        if function_descriptions:
            functions_text = "You can call the following functions:\n\n" + \
                             "\n".join([f"- {desc}" for desc in function_descriptions]) + \
                             "\n\nTo call a function, use a JSON format like this:" + \
                             '\n```json\n{"name": "function_name", "arguments": {"arg1": "value1", "arg2": "value2"}}\n```\n'
        
        return f"""You are {self.name}, an AI assistant with the following capabilities:

{capabilities_text}

{functions_text}

When responding to user requests, you should determine which capabilities to use and which functions to call.
If you need to call a function, format your response as a JSON function call.
If you've received function results or no function calls are needed, provide a helpful response to the user.
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
    
    def _generate_default_response(self, prompt: str) -> str:
        """Generate a default response when no functions are registered."""
        capabilities_text = ", ".join(self.capabilities)
        return f"I'm {self.name}. For your request '{prompt}', I would use these capabilities: {capabilities_text}"
    
    def _generate_with_openai(self, system_message: str, user_message: str) -> str:
        """Generate a response using OpenAI API."""
        try:
            # Prepare conversation history in OpenAI format
            messages = [{"role": "system", "content": system_message}]
            
            # Add conversation history
            for msg in self.conversation_history:
                messages.append(msg)
            
            # Add the current user message
            messages.append({"role": "user", "content": user_message})
            
            logger.debug(f"Sending {len(messages)} messages to OpenAI")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            return f"Error generating response with OpenAI: {str(e)}"
    
    def _generate_with_anthropic(self, system_message: str, user_message: str) -> str:
        """Generate a response using Anthropic API."""
        try:
            # Prepare messages
            messages = []
            
            # Add conversation history
            for msg in self.conversation_history:
                if msg["role"] == "function":
                    messages.append({
                        "role": "assistant",
                        "content": f"Function {msg['name']} returned: {msg['content']}"
                    })
                else:
                    messages.append(msg)
            
            # Add the current user message
            messages.append({"role": "user", "content": user_message})
            
            logger.debug(f"Sending request to Anthropic with {len(messages)} messages")
            
            response = self.client.messages.create(
                model=self.model,
                system=system_message,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.content[0].text
        except Exception as e:
            logger.error(f"Anthropic API error: {str(e)}")
            return f"Error generating response with Anthropic: {str(e)}"


def create_agent(name="TeenAGI", provider="openai", model=None, log_level="INFO", log_to_file=False):
    """
    Factory function to create a TeenAGI instance.
    
    Args:
        name (str): Name of the agent
        provider (str): "openai" or "anthropic"
        model (str, optional): Model to use
        log_level (str): Logging level
        log_to_file (bool): Whether to log to a file
        
    Returns:
        TeenAGI: An initialized TeenAGI instance
    """
    return TeenAGI(name=name, provider=provider, model=model, 
                  log_level=log_level, log_to_file=log_to_file) 