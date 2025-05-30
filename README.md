# TeenAGI

A Python package for building AI agents capable of making multiple function calls in sequence. Inspired by BabyAGI but with more advanced capabilities.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
  - [Python API](#python-api)
  - [Command Line Interface](#command-line-interface)
- [Development](#development)
  - [Setup Development Environment](#setup-development-environment)
- [License](#license)
- [Contributing](#contributing)

## Installation

```bash
pip install teenagi
```

## Usage

### Python API

```python
from teenagi import TeenAGI, create_agent

# Create an agent with a custom name and OpenAI integration
agent = TeenAGI(
    name="Research Assistant",
    api_key="your_openai_api_key",  # Or set OPENAI_API_KEY environment variable
    provider="openai",  # "openai" or "anthropic"
    model="gpt-4-turbo"  # Optional, defaults to "gpt-3.5-turbo" for OpenAI
)

# Add capabilities to the agent
agent.learn("can search the web for information")
agent.learn("can summarize long documents")

# Get a response that might require multiple function calls
response = agent.respond("Find and summarize recent research on climate change")
print(response)

# Alternative: use the factory function
specialized_agent = create_agent(
    name="DataAnalyst",
    provider="anthropic",
    model="claude-3-opus-20240229"
)
```

### Command Line Interface

TeenAGI includes a CLI for quick interactions:

```bash
# Basic usage
teenagi --name "ResearchBot" --capabilities "can search the web" "can summarize text" "Find recent papers on quantum computing"

# Using with OpenAI
teenagi --provider openai --api-key "your_openai_api_key" --model "gpt-4" "Explain quantum entanglement"

# Using with Anthropic
teenagi --provider anthropic --api-key "your_anthropic_api_key" --model "claude-3-sonnet-20240229" "Explain quantum entanglement"
```

You can also store your API keys in a `.env` file:

```
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/jordan/teen-agi.git
cd teen-agi

# Install dependencies with Poetry
poetry install

# Run tests
poetry run pytest
```

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
