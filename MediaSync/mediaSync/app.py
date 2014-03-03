import urllib.request
from mediaSync.source import Source
from mediaSync.item import Item
from xml.etree.ElementTree import XML
from mediaSync.httpClientFactory import HttpClientFactory
from mediaSync.sqlLiteClientFactory import SqlLiteClientFactory

class App(object):
    
    downloadHistoryTableName = "download_history"
    
    def __init__(self, configuration):
        self.configuration = configuration
        self.destinations = configuration.destinations
        self.sources = configuration.sources
        self.filters = configuration.filters
        self.httpClientFactory = HttpClientFactory()
        self.sqlLiteClientFactory = SqlLiteClientFactory()
        
    def chooseFilesToDownload(self, items, destination):
        
        client = self.httpClientFactory.create()
        
        for item in items:
            
            request = client.createRequest(item.link)
            
            response = client.getResponse(request)
            
            filename = response.location
        
        
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
    
    def checkExists(self, item):
        
        client = self.sqlLiteClientFactory.create(App.downloadHistoryTableName)
        
        pk = item.link
        
        result = client.exists(pk)
        
        client.close()
        
        return result
        
    
    def markDownloaded(self, item):
        
        client = self.sqlLiteClientFactory.create(App.downloadHistoryTableName)
        
        client.insert(item.link, item)
        
        client.close()
        