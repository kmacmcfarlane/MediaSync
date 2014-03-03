from mediaSync.test.mockSqlLiteClient import MockSqlLiteClient

class MockSqlLiteClientFactory(object):

    def __init__(self):
        
        pass
    
    def create(self, tableName):

        return MockSqlLiteClient(tableName)
    
