"""
Function registry for TeenAGI.

This module allows registering Python functions that can be called by TeenAGI agents.
"""

import inspect
import json
from typing import Any, Callable, Dict, List, Optional, Union


class FunctionRegistry:
    """Registry for functions that can be called by TeenAGI agents."""
    
    def __init__(self):
        """Initialize an empty function registry."""
        self.functions: Dict[str, Dict[str, Any]] = {}
    
    def register(self, func: Optional[Callable] = None, *, 
                 name: Optional[str] = None, 
                 description: Optional[str] = None) -> Callable:
        """
        Register a function to be callable by TeenAGI agents.
        
        Can be used as a decorator:
        
        @registry.register(description="Search the web for information")
        def search_web(query: str) -> str:
            ...
            
        Or called directly:
        
        registry.register(search_web, description="Search the web for information")
        
        Args:
            func: The function to register
            name: Optional custom name for the function (defaults to the function name)
            description: Description of what the function does
            
        Returns:
            The original function (for decorator usage)
        """
        def decorator(f: Callable) -> Callable:
            func_name = name or f.__name__
            func_doc = description or f.__doc__ or "No description provided"
            
            # Get function signature
            sig = inspect.signature(f)
            parameters = {}
            
            for param_name, param in sig.parameters.items():
                # Skip self for methods
                if param_name == 'self':
                    continue
                    
                param_type = "string"
                if param.annotation != inspect.Parameter.empty:
                    if param.annotation == int:
                        param_type = "integer"
                    elif param.annotation == float:
                        param_type = "number"
                    elif param.annotation == bool:
                        param_type = "boolean"
                    elif param.annotation == list or param.annotation == List:
                        param_type = "array"
                    elif param.annotation == dict or param.annotation == Dict:
                        param_type = "object"
                
                parameters[param_name] = {
                    "type": param_type,
                    "description": "",  # Could parse from docstring in a more advanced implementation
                    "required": param.default == inspect.Parameter.empty
                }
            
            # Create function schema (compatible with OpenAI function calling format)
            self.functions[func_name] = {
                "function": f,
                "schema": {
                    "name": func_name,
                    "description": func_doc,
                    "parameters": {
                        "type": "object",
                        "properties": parameters,
                        "required": [p for p, v in parameters.items() if v["required"]]
                    }
                }
            }
            return f
        
        # Handle both decorator and direct call patterns
        if func is None:
            return decorator
        return decorator(func)
    
    def get_function_schemas(self) -> List[Dict[str, Any]]:
        """
        Get all registered function schemas in OpenAI-compatible format.
        
        Returns:
            List of function schemas
        """
        return [f["schema"] for f in self.functions.values()]
    
    def get_function_descriptions(self) -> List[str]:
        """
        Get human-readable descriptions of all registered functions.
        
        Returns:
            List of function descriptions
        """
        descriptions = []
        for name, func_info in self.functions.items():
            schema = func_info["schema"]
            params = []
            for param_name, param_info in schema["parameters"]["properties"].items():
                required = "(required)" if param_name in schema["parameters"].get("required", []) else "(optional)"
                params.append(f"{param_name} {required}")
            
            param_str = ", ".join(params)
            descriptions.append(f"{name}({param_str}): {schema['description']}")
        
        return descriptions
    
    def execute_function(self, name: str, **kwargs) -> Any:
        """
        Execute a registered function with the given arguments.
        
        Args:
            name: Name of the function to execute
            **kwargs: Arguments to pass to the function
            
        Returns:
            The result of the function call
            
        Raises:
            ValueError: If the function is not registered
            TypeError: If the arguments don't match the function signature
        """
        if name not in self.functions:
            raise ValueError(f"Function '{name}' is not registered")
        
        return self.functions[name]["function"](**kwargs)
    
    def parse_and_execute(self, function_call: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse a function call specification and execute it.
        
        Args:
            function_call: Dictionary with 'name' and 'arguments' keys
            
        Returns:
            Dictionary with 'name', 'result', and 'error' keys
        """
        name = function_call.get("name")
        args_str = function_call.get("arguments", "{}")
        
        if not name:
            return {"error": "Function name not provided"}
        
        try:
            # Parse arguments from JSON string
            kwargs = json.loads(args_str)
            
            # Execute function
            result = self.execute_function(name, **kwargs)
            
            return {
                "name": name,
                "result": result,
                "error": None
            }
        except json.JSONDecodeError:
            return {
                "name": name,
                "result": None,
                "error": f"Invalid arguments JSON: {args_str}"
            }
        except Exception as e:
            return {
                "name": name,
                "result": None,
                "error": str(e)
            }


# Create a global function registry
registry = FunctionRegistry() 