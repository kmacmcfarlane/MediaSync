import urllib.request
from mediaSync.source import Source
from mediaSync.item import Item
from xml.etree.ElementTree import XML

class App(object):
    def __init__(self, configuration):
        self.configuration = configuration
        self.destinations = configuration.destinations
        self.sources = configuration.sources
        self.filters = configuration.filters
        
    def pullBytes(self, source):
        
        uri = source.uri
        
        # Construct HTTP client
        client = urllib.request.urlopen(uri)
        
        # Read contents and return
        return client.read()
    
    
    def parseBytes(self, feedBytes):
        
        root = XML(feedBytes)
        channelElement = root[0]

        itemElements = channelElement.findall('item')
        
        items = []
        
        for itemElement in itemElements:
            
            item = Item(itemElement)
            
            items.append(item)

        return items
    
    def filterItems(self, items, filters):
        
        if items is None:
            raise Exception('items cannot be None')
        
        if filters is None:
            raise Exception('filters cannot be None')
        
        for aFilter in filters:
            
            items = aFilter.filter(items)
        
        return items