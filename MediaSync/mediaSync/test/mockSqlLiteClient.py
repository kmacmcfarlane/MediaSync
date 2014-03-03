
class MockSqlLiteClient(object):
    
    databases = dict()
       
    def __init__(self, tableName):
        
        self.tableName = tableName
        
        pass
    
    def getDatabase(self):
        
        if self.tableName not in MockSqlLiteClient.databases:
            MockSqlLiteClient.databases[self.tableName] = dict()
            
        return MockSqlLiteClient.databases[self.tableName]
    
    def exists(self, pk):
        
        if pk in self.getDatabase():
            return self.getDatabase()[pk]
        else:
            return False
        
    def fetch(self, pk):
        
        if pk in self.getDatabase():
            return self.getDatabase()[pk]
        else:
            return None
    
    def insert(self, pk, item):
        
        self.getDatabase()[pk] = item
    
    def close(self):
        
        pass