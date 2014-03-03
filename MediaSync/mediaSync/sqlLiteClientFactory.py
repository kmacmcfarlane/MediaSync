from mediaSync.sqlLiteClient import SqlLiteClient

class SqlLiteClientFactory:
    
    def __init__(self):
        
        pass
    
    def create(self, tableName):
        return SqlLiteClient(tableName)