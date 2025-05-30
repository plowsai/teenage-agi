"""
Tests for the TeenAGI package.
"""

import pytest
from teenagi import TeenAGI, create_agent


def test_teenagi_init():
    """Test TeenAGI initialization."""
    agi = TeenAGI(name="TestAGI", age=15)
    assert agi.name == "TestAGI"
    assert agi.age == 15
    assert agi.knowledge_base == []


def test_teenagi_invalid_age():
    """Test TeenAGI with invalid age."""
    with pytest.raises(ValueError):
        TeenAGI(age=20)  # Too old
    
    with pytest.raises(ValueError):
        TeenAGI(age=12)  # Too young


def test_teenagi_learn():
    """Test TeenAGI learning functionality."""
    agi = TeenAGI()
    
    # Test learning something valid
    assert agi.learn("Python is a programming language")
    assert len(agi.knowledge_base) == 1
    
    # Test learning empty string (should fail)
    assert not agi.learn("")
    assert len(agi.knowledge_base) == 1


def test_teenagi_respond():
    """Test TeenAGI response generation."""
    agi = TeenAGI(name="ResponderAGI", age=16)
    
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
    assert isinstance(agi, TeenAGI)
    assert agi.name == "FactoryAGI"
    assert agi.age == 17 