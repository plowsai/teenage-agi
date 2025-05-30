#!/usr/bin/env python
"""
Command Line Interface for TeenAGI.
"""

import argparse
import os
import sys
from dotenv import load_dotenv, find_dotenv

from teenagi import TeenAGI, create_agent, __version__

# Load environment variables from .env file
env_file = find_dotenv()
if not env_file:
    print("Warning: No .env file found. Please create one with your API keys.")
    print("Example:")
    print("  OPENAI_API_KEY=your_openai_api_key_here")
    print("  ANTHROPIC_API_KEY=your_anthropic_api_key_here")
else:
    load_dotenv(env_file)


def main():
    """Main CLI entrypoint for TeenAGI."""
    parser = argparse.ArgumentParser(description="TeenAGI - An agent capable of making multiple function calls")
    parser.add_argument('--version', action='version', version=f'TeenAGI v{__version__}')
    parser.add_argument('--name', type=str, default="TeenAGI", help="Name for the agent")
    parser.add_argument('--capabilities', type=str, nargs='*', help="Capabilities to add to the agent")
    parser.add_argument('--provider', type=str, choices=['openai', 'anthropic'], default='openai',
                        help="AI provider to use (openai or anthropic)")
    parser.add_argument('--model', type=str, help="Model to use (provider-specific)")
    parser.add_argument('prompt', nargs='?', help="Prompt to send to the agent")
    
    args = parser.parse_args()
    
    if not args.prompt and not args.capabilities:
        parser.print_help()
        return
    
    # Check for required API keys
    if args.provider == 'openai' and not os.environ.get("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found in .env file.")
        print("Please create a .env file with your OpenAI API key.")
        return 1
    elif args.provider == 'anthropic' and not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY not found in .env file.")
        print("Please create a .env file with your Anthropic API key.")
        return 1
    
    try:
        # Create an agent
        agent = create_agent(
            name=args.name,
            provider=args.provider,
            model=args.model
        )
        
        # Add capabilities if provided
        if args.capabilities:
            print(f"Adding capabilities to {args.name}:")
            for capability in args.capabilities:
                success = agent.learn(capability)
                if success:
                    print(f"  ✓ {capability}")
                else:
                    print(f"  ✗ Failed to add: {capability}")
        
        # If a prompt is provided, get a response
        if args.prompt:
            print("\nProcessing request:", args.prompt)
            print("\nResponse:")
            response = agent.respond(args.prompt)
            print(response)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 