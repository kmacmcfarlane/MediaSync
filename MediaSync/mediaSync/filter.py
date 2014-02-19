from mediaSync.fileFilter import FileFilter
from mediaSync.expressionFilter import ExpressionFilter

class Filter(object):

    
    def __init__(self, rawConfiguration, name):
        
        self.name = name
            
        if "file" in rawConfiguration:
            self.file = rawConfiguration["file"]
        else:
            self.file = None
        
        if "expression" in rawConfiguration:
            self.expression = rawConfiguration["expression"]
        else:
            self.expression = None

        self.type = rawConfiguration["type"]
        self.property = rawConfiguration["property"]
        
        if self.file is not None:
            self.filterImpl = FileFilter(self.file, self.property)
        elif self.expression is not None:
            self.filterImpl = ExpressionFilter(self.expression, self.property)
        else:
            raise Exception('Configuration Error, you must have either an \'expression\' or a \'file\' property in your filter: ' + self.name)

    def filter(self, items):
        
        results = []
        
        for item in items:
            if self.filterImpl.filter(item):
                results.append(item)
        
        return results