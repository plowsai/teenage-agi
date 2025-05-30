# TeenageAGI

A Python package inspired by BabyAGI(babyagi.org).

## Installation

```bash
pip install teenageagi
```

## Usage

```python
from teenageagi import TeenageAGI, create_agent

# Create a teenage AGI with custom name and age
agent = TeenageAGI(name="Alex", age=16)

# Add knowledge to the agent
agent.learn("Python is a versatile programming language")
agent.learn("Machine learning is a subset of artificial intelligence")

# Get a response from the agent
response = agent.respond("Tell me about programming")
print(response)

# Alternative: use the factory function
factory_agent = create_agent(name="Sam", age=17)
```

## Features

- Create AGI agents with customizable names and teenage ages (13-19)
- Add knowledge to your AGI's knowledge base
- Generate responses based on accumulated knowledge
- Simple and intuitive API

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/jordan/teenage-agi.git
cd teenage-agi

# Install dependencies with Poetry
poetry install

# Run tests
poetry run pytest
```

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
