"""
Tests for the TeenAGI package.
"""

import pytest
from teenagi import TeenAGI, create_agent


def test_teenagi_init():
    """Test TeenAGI initialization."""
    agent = TeenAGI(name="TestAgent")
    assert agent.name == "TestAgent"
    assert agent.capabilities == []


def test_teenagi_learn():
    """Test TeenAGI learning functionality."""
    agent = TeenAGI()
    
    # Test adding a valid capability
    assert agent.learn("can search the web")
    assert len(agent.capabilities) == 1
    
    # Test adding an empty capability (should fail)
    assert not agent.learn("")
    assert len(agent.capabilities) == 1
    
    # Test adding multiple capabilities
    agent.learn("can summarize text")
    agent.learn("can translate languages")
    assert len(agent.capabilities) == 3


def test_teenagi_respond():
    """Test TeenAGI response generation."""
    agent = TeenAGI(name="ResponderAgent")
    
    # Response with no capabilities
    response = agent.respond("Hello")
    assert "ResponderAgent" in response
    assert "don't have any capabilities" in response
    
    # Add capabilities and test response
    agent.learn("can search the web")
    agent.learn("can summarize text")
    response = agent.respond("Find and summarize an article")
    assert "ResponderAgent" in response
    assert "search the web" in response
    assert "summarize text" in response


def test_create_agent():
    """Test the create_agent factory function."""
    agent = create_agent(name="FactoryAgent")
    assert isinstance(agent, TeenAGI)
    assert agent.name == "FactoryAgent"
    assert agent.capabilities == [] 