import re
class ExpressionFilter:
    
    def __init__(self, expression, attributeName):
        
        self.expression = re.compile(expression, flags=re.IGNORECASE)
        self.attributeName = attributeName
        
        
    def filter(self, item):
        
        if self.expression.search(getattr(item, self.attributeName)) is not None:
            return True
        else:
            return False
        