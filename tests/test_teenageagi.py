"""
Tests for the TeenageAGI package.
"""

import pytest
from teenageagi import TeenageAGI, create_agent


def test_teenageagi_init():
    """Test TeenageAGI initialization."""
    agi = TeenageAGI(name="TestAGI", age=15)
    assert agi.name == "TestAGI"
    assert agi.age == 15
    assert agi.knowledge_base == []


def test_teenageagi_invalid_age():
    """Test TeenageAGI with invalid age."""
    with pytest.raises(ValueError):
        TeenageAGI(age=20)  # Too old
    
    with pytest.raises(ValueError):
        TeenageAGI(age=12)  # Too young


def test_teenageagi_learn():
    """Test TeenageAGI learning functionality."""
    agi = TeenageAGI()
    
    # Test learning something valid
    assert agi.learn("Python is a programming language")
    assert len(agi.knowledge_base) == 1
    
    # Test learning empty string (should fail)
    assert not agi.learn("")
    assert len(agi.knowledge_base) == 1


def test_teenageagi_respond():
    """Test TeenageAGI response generation."""
    agi = TeenageAGI(name="ResponderAGI", age=16)
    
    # Response with empty knowledge base
    response = agi.respond("Hello")
    assert "ResponderAGI" in response
    assert "16" in response
    assert "don't know much" in response
    
    # Add knowledge and test response
    agi.learn("Important information")
    response = agi.respond("Tell me something")
    assert "ResponderAGI" in response
    assert "16" in response
    assert "Based on what I know" in response


def test_create_agent():
    """Test the create_agent factory function."""
    agi = create_agent(name="FactoryAGI", age=17)
    assert isinstance(agi, TeenageAGI)
    assert agi.name == "FactoryAGI"
    assert agi.age == 17 