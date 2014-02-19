import re

class FileFilter(object):
    
    def __init__(self, filename, attributeName):
        
        self.attributeName = attributeName
        
        self.file = open(filename, mode='r')        
        
        self.expressions = []
        
        for expression in self.file:
            self.expressions.append(re.compile(expression.strip('\n'), flags=re.IGNORECASE))
            
        self.file.close()
        
    def filter(self, item):

        for expression in self.expressions:
            value = getattr(item, self.attributeName)
            
            if expression.search(value) is not None:
                return True
        
        return False
    