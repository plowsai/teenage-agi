#!/usr/bin/env python
"""
Command Line Interface for TeenAGI.
"""

import argparse
import os
import sys
from dotenv import load_dotenv

from teenagi import TeenAGI, create_agent, __version__

# Load environment variables from .env file if present
load_dotenv()


def main():
    """Main CLI entrypoint for TeenAGI."""
    parser = argparse.ArgumentParser(description="TeenAGI - An agent capable of making multiple function calls")
    parser.add_argument('--version', action='version', version=f'TeenAGI v{__version__}')
    parser.add_argument('--name', type=str, default="TeenAGI", help="Name for the agent")
    parser.add_argument('--capabilities', type=str, nargs='*', help="Capabilities to add to the agent")
    parser.add_argument('--provider', type=str, choices=['openai', 'anthropic'], default='openai',
                        help="AI provider to use (openai or anthropic)")
    parser.add_argument('--api-key', type=str, help="API key for the selected provider")
    parser.add_argument('--model', type=str, help="Model to use (provider-specific)")
    parser.add_argument('prompt', nargs='?', help="Prompt to send to the agent")
    
    args = parser.parse_args()
    
    if not args.prompt and not args.capabilities:
        parser.print_help()
        return
    
    # Get API key from args, or environment variable
    api_key = args.api_key
    if not api_key:
        if args.provider == 'openai':
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                print("Error: OpenAI API key not provided. Use --api-key or set OPENAI_API_KEY environment variable.")
                return 1
        elif args.provider == 'anthropic':
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                print("Error: Anthropic API key not provided. Use --api-key or set ANTHROPIC_API_KEY environment variable.")
                return 1
    
    try:
        # Create an agent
        agent = create_agent(
            name=args.name,
            api_key=api_key,
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