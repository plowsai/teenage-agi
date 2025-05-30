"""
Core functionality for the TeenageAGI package.
"""

class TeenageAGI:
    """
    Main class for TeenageAGI functionality.
    """
    
    def __init__(self, name="TeenageAGI", age=16):
        """
        Initialize a TeenageAGI instance.
        
        Args:
            name (str): Name of the AGI
            age (int): Age of the AGI (must be between 13-19)
        """
        self.name = name
        if not (13 <= age <= 19):
            raise ValueError("Age must be between 13 and 19 for a teenage AGI")
        self.age = age
        self.knowledge_base = []
    
    def learn(self, information):
        """
        Add information to the AGI's knowledge base.
        
        Args:
            information (str): Information to learn
        
        Returns:
            bool: True if learning was successful
        """
        if not information:
            return False
        
        self.knowledge_base.append(information)
        return True
    
    def respond(self, prompt):
        """
        Generate a response based on knowledge.
        
        Args:
            prompt (str): Input prompt
            
        Returns:
            str: Generated response
        """
        if not self.knowledge_base:
            return f"Hi, I'm {self.name}, a {self.age}-year-old AGI. I don't know much yet."
        
        return f"Hi, I'm {self.name}, a {self.age}-year-old AGI. Based on what I know, here's my response to '{prompt}': ..."

def create_agent(name="TeenageAGI", age=16):
    """
    Factory function to create a TeenageAGI instance.
    
    Args:
        name (str): Name of the AGI
        age (int): Age of the AGI
        
    Returns:
        TeenageAGI: An initialized TeenageAGI instance
    """
    return TeenageAGI(name=name, age=age) 