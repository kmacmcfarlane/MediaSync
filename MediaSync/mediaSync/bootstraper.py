from mediaSync.configuration import Configuration
from mediaSync.app import App

class Bootstraper(object):
    
    def __init__(self):
        
        self._app = None
        self._configuration = None
        self._isInitialized = False
    
    def boot(self):
        
        if(False == self._isInitialized):
            self._configuration = Configuration("./")
        
            self._app = App(self._configuration)
            
            self._isInitiazited = True

    @property
    def app(self):
        return self._app
    
    @property
    def configuration(self):
        return self._configuration
    
    


