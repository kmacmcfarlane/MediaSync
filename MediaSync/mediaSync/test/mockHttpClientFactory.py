from mediaSync.test.mockHttpClient import MockHttpClient

class MockHttpClientFactory:

    def __init__(self):
        pass
    
    def create(self):
        
        return MockHttpClient()