import json
from mediaSync.source import Source
from mediaSync.destination import Destination
from mediaSync.filter import Filter

class Configuration(object):
    def __init__(self, searchPath):
        self.searchPaths = searchPath
        self.configurationFilename = "mediasync.conf"
        self.sources = {}
        self.destinations = {}
        self.filters = {}
        
        file = self.openConfFile(searchPath)
        
        self.parseFile(file)
                
    
    def openConfFile(self, searchPath):
            
        if(False == searchPath.endswith("/")):
            searchPath = searchPath + "/"
                
        fullPath = searchPath + self.configurationFilename

        return open(fullPath, mode='r')
    
    def parseFile(self, file):
        data = file.read()
        rawConfiguration = json.loads(data)
        
        file.close()
        
        for key in rawConfiguration["sources"]:
            
            source = rawConfiguration["sources"][key]
            
            self.sources[key] = Source(source, key)
        
        
        for key in rawConfiguration["destinations"]:
            
            destination = rawConfiguration["destinations"][key]
            
            self.destinations[key] = Destination(destination, key)
        
        
        for key in rawConfiguration["filters"]:
            
            filterConfiguration = rawConfiguration["filters"][key]
            
            try:
                self.filters[key] = Filter(filterConfiguration, key)
            except FileNotFoundError:
                print("FilterFile not specified for filter: " + key)

        return rawConfiguration
