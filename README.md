# TeenAGI

A Python package for building AI agents capable of making multiple function calls in sequence. Inspired by BabyAGI but with more advanced capabilities.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
  - [Setting Up API Keys](#setting-up-api-keys)
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

### Setting Up API Keys

TeenAGI requires API keys to be stored in a `.env` file in your project directory. Create a file named `.env` with the following content:

```
# For OpenAI GPT models
OPENAI_API_KEY=your_openai_api_key_here

# For Anthropic Claude models
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

This file should be kept secure and never committed to version control.

### Python API

```python
from teenagi import TeenAGI, create_agent

# TeenAGI will automatically load API keys from your .env file
agent = TeenAGI(
    name="Research Assistant",
    provider="openai",  # "openai" or "anthropic"
    model="gpt-4.1
)

# Add capabilities to the agent
agent.learn("can search the web for information")
agent.learn("can summarize long documents")

# Get a response that might require multiple function calls
response = agent.respond("Find and summarize recent research on climate change")
print(response)

# Alternative: use the factory function with Anthropic
specialized_agent = create_agent(
    name="DataAnalyst",
    provider="anthropic",
    model="claude-3-opus-20240229"
)
```

### Command Line Interface

TeenAGI includes a CLI for quick interactions. It will automatically use the API keys from your `.env` file:

```bash
# Basic usage
teenagi --name "ResearchBot" --capabilities "can search the web" "can summarize text" "Find recent papers on quantum computing"

# Using with OpenAI (requires OPENAI_API_KEY in .env)
teenagi --provider openai --model "gpt-4" "Explain quantum entanglement"

# Using with Anthropic (requires ANTHROPIC_API_KEY in .env)
teenagi --provider anthropic --model "claude-3-sonnet-20240229" "Explain quantum entanglement"
```

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/jordan/teen-agi.git
cd teen-agi

# Install dependencies with Poetry
poetry install

# Create a .env file with your API keys
echo "OPENAI_API_KEY=your_key_here" > .env
# or
echo "ANTHROPIC_API_KEY=your_key_here" > .env

# Run tests
poetry run pytest
```

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
