'''
Created on Jul 21, 2013

@author: Kyle
'''
import unittest
import urllib.request
from mediaSync.configuration import Configuration
from mediaSync.app import App
import os
from mediaSync.source import Source
from mediaSync.destination import Destination
from mediaSync.filter import Filter
from mediaSync.bootstraper import Bootstraper
from sqlite3.dbapi2 import Time
from xml.etree.ElementTree import Element, XML
import datetime
import time
import copy
from urllib.parse import urlparse
from mediaSync.item import Item
from mediaSync.test.mockHttpClientFactory import MockHttpClientFactory
from mediaSync.test.mockSqlLiteClientFactory import MockSqlLiteClientFactory

class TestMediaSync(unittest.TestCase):
    
    def testLoadConfiguration(self):
        
        searchPath = "./" # mediaSync/test
        configuration = Configuration(searchPath)
        
        configurationFile = configuration.openConfFile(searchPath)
        
        self.assertIsNotNone(configurationFile, "Test configuration file shall be present. CWD=" + os.getcwd())
        
        rawConfiguration = configuration.parseFile(configurationFile)
        
        self.assertIsNotNone(rawConfiguration, "The configuration file shall be parsed as JSON.")
        self.assertIsNotNone(rawConfiguration["sources"], "The configuration file shall contain a source." )
        self.assertIsNotNone(rawConfiguration["destinations"], "The configuration file shall contain a destination." )
        self.assertIsNotNone(rawConfiguration["filters"], "The configuration file shall contain filters." )
        
        self.assertIsNotNone(configuration.sources, "The configuration object shall contain a source.")
        self.assertIsNotNone(configuration.destinations, "The configuration object shall contain a destination.")
        self.assertIsNotNone(configuration.filters, "The configuration object shall contain filters.")


        self.assertEqual("btn", configuration.sources["btn"].name, "The source must contain the correct name.")
        self.assertEqual("https://broadcasthe.net/feeds.php?feed=torrents_episode&user=1485399&auth=4944d992c85b5ff93f1bb715ad68c671&passkey=tkfh3yf4o60c8nlyxny0x7lrqpg77k1a&authkey=ff9be6ee72a2a26d365f4454a98db5f6", configuration.sources["btn"].uri, "The source must contain the correct URI.")
        self.assertEqual("start.tv", configuration.sources["btn"].directory, "The source must contain the correct descriptor directory.")
        
        self.assertEqual("tv", configuration.destinations["tv"].name, "The destination must contain the correct name.")
        self.assertEqual("download.tv", configuration.destinations["tv"].directory, "The destination must contain the correct URI.")

        self.assertTrue(len(configuration.filters) > 0)
        
        self.assertEqual("filter.txt", configuration.filters["nameRegex"].file, "The filter must contain the correct file.")
        self.assertEqual("regex", configuration.filters["nameRegex"].type, "The filter must contain the correct type.")
        self.assertEqual("title", configuration.filters["nameRegex"].property, "The filter must contain the correct type.")
        
        self.assertEqual("\[\ 720p\ \]", configuration.filters["resolutionRegex"].expression, "The filter must contain the correct file.")
        self.assertEqual("regex", configuration.filters["resolutionRegex"].type, "The filter must contain the correct type.")
        self.assertEqual("title", configuration.filters["resolutionRegex"].property, "The filter must contain the correct type.")
                
        # Bad File
        badFile = configuration.openConfFile("./badConfiguration")
        
        self.assertRaises(ValueError, configuration.parseFile, badFile)
        
    def testLoadSource(self):
        configuration = Configuration("./")
        rawConfiguration = configuration.parseFile(configuration.openConfFile("./"))
        
        source = Source(rawConfiguration["sources"]["btn"], "btn")
        
        self.assertEqual("btn", source.name)
        self.assertEqual("https://broadcasthe.net/feeds.php?feed=torrents_episode&user=1485399&auth=4944d992c85b5ff93f1bb715ad68c671&passkey=tkfh3yf4o60c8nlyxny0x7lrqpg77k1a&authkey=ff9be6ee72a2a26d365f4454a98db5f6", source.uri)
        self.assertEqual("start.tv", source.directory)
        self.assertEqual("nameRegex,resolutionRegex", source.filters)
        
        
        globalContext = Bootstraper()
        globalContext.boot()
        
        app = globalContext.app
        
        self.assertEqual("btn", app.sources["btn"].name)
        self.assertEqual("https://broadcasthe.net/feeds.php?feed=torrents_episode&user=1485399&auth=4944d992c85b5ff93f1bb715ad68c671&passkey=tkfh3yf4o60c8nlyxny0x7lrqpg77k1a&authkey=ff9be6ee72a2a26d365f4454a98db5f6", app.sources["btn"].uri)
        self.assertEqual("start.tv", app.sources["btn"].directory)
        self.assertEqual("nameRegex,resolutionRegex", app.sources["btn"].filters)
        
    def testLoadDestination(self):
        
        configuration = Configuration("./")
        
        rawConfiguration = configuration.parseFile(configuration.openConfFile("./"))
        
        destination = Destination(rawConfiguration["destinations"]["tv"], "tv")
        
        self.assertEqual("tv", destination.name)
        self.assertEqual("download.tv", destination.directory)
        
        
        globalContext = Bootstraper()
        globalContext.boot()
        
        app = globalContext.app
        
        self.assertEqual("tv", destination.name)
        self.assertEqual("download.tv", destination.directory)
    
    def testLoadFilter(self):
        configuration = Configuration("./")
        
        rawConfiguration = configuration.parseFile(configuration.openConfFile("./"))
        
        nameFilter = Filter(rawConfiguration["filters"]["nameRegex"], "nameRegex")
        
        self.assertEqual("filter.txt", nameFilter.file)
        self.assertEqual("regex", nameFilter.type)
        self.assertEqual("title", nameFilter.property)
        
        resolutionFilter = Filter(rawConfiguration["filters"]["resolutionRegex"], "resolutionRegex")
        
        self.assertEqual("\[\ 720p\ \]", resolutionFilter.expression)
        self.assertEqual("regex", resolutionFilter.type)
        self.assertEqual("title", resolutionFilter.property)
        
                
        globalContext = Bootstraper()
        globalContext.boot()
        
        app = globalContext.app
        
        self.assertIsNotNone(app.filters["nameRegex"])
        
        self.assertEqual("filter.txt", app.filters["nameRegex"].file)
        self.assertEqual("regex", app.filters["nameRegex"].type)
        self.assertEqual("title", app.filters["nameRegex"].property)
        
        self.assertIsNotNone(app.filters["resolutionRegex"])
        
        self.assertEqual("\[\ 720p\ \]", app.filters["resolutionRegex"].expression)
        self.assertEqual("regex", app.filters["resolutionRegex"].type)
        self.assertEqual("title", app.filters["resolutionRegex"].property)
        
    def testAppInitialize(self):
        
        searchPaths = "./"
        configuration = Configuration(searchPaths)
        
        app = App(configuration)
                
        self.assertTrue([] != app.destinations, "App shall create destination media libraries")
        self.assertTrue([] != app.sources, "App shall create source media libraries")
        
    def testBootstraper(self):
        
        globalContext = Bootstraper()
        
        globalContext.boot();
        
        self.assertIsNotNone(globalContext.app, "Bootstraper shall construct the app object.")
        self.assertIsNotNone(globalContext.configuration, "Bootstraper shall construct a configuration.")
        
        
    def testPullParseData(self):
        
        globalContext = Bootstraper()
        globalContext.boot();
        app = globalContext.app
        
        assert isinstance(app, App)
        
        rawFeedBytes =  open('./feed.xml', mode='r', encoding='utf-8').read() #app.pullBytes(app.source)
        
        self.assertIsNotNone(rawFeedBytes)
        self.assertTrue(len(rawFeedBytes) > 0, "The length of the rss feed shall not be 0.")
        
        feedTree = XML(rawFeedBytes)
        
        self.assertIsNotNone(feedTree)
        
        self.assertTrue(feedTree[0].tag == "channel")
        
        itemElements = feedTree[0].findall('item')
        self.assertTrue(0 < len(itemElements))
        
        for itemElement in itemElements:
            
            self.assertIsNotNone(itemElement.find('title'))
            self.assertIsNotNone(itemElement.find('description'))
            self.assertIsNotNone(itemElement.find('link'))
        
        items = app.parseBytes(rawFeedBytes)
        
        for item in items:
            
            self.assertIsNotNone(item)
            self.assertIsNotNone(item.title)
            self.assertIsNotNone(item.description)
            self.assertIsNotNone(item.timestamp)
            self.assertIsInstance(item.timestamp, time.struct_time)
            self.assertIsNotNone(item.rawTimestamp)
            self.assertIsNotNone(item.link)

    def createPositiveItem(self):
        
        
        
        positiveItem = Item(None)
        
        positiveItem.title = "Satisfaction (2013) - S01E12 [ 2013 ] [ MKV | x264 | HDTV | 720p | Scene | FastTorrent ] [ Uploader: Anonymous ]  [ Satisfaction.CA.S01E12.720p.HDTV.x264-KILLERS ]"
        positiveItem.link = "http://broadcasthe.net/torrents.php?action=download&amp;authkey=ff9be6ee72a2a26d365f4454a98db5f6&amp;torrent_pass=tkfh3yf4o60c8nlyxny0x7lrqpg77k1a&amp;id=306735"
        positiveItem.description = "faoeru"
#"Episode Name: Daddy Issues<br />\
#Season: 1<br />\
#Episode: 12<br />\
#Aired: 2013-09-09<br />\
#<br />\
#Episode Overview:<br />\
#When Maggie�s dad comes to town, Jason and Mark vie for his attention but discover a secret he�s been keeping in the process. Meanwhile the new, hardworking waitress at the bar quickly becomes Maggie�s nemesis.<br />\
#<br />\
#Episode Image <br />\
#[img=https://cdn2.broadcasthe.net/tvdb/banners/episodes/269538/4630029.jpg]"
        positiveItem.rawTimestamp = "Tue, 10 Sep 2013 00:38:35 +0000"
        positiveItem.timestamp = time.strptime(positiveItem.rawTimestamp, "%a, %d %b %Y %H:%M:%S %z")
        
        return positiveItem

    def createNegativeItem(self):
        
        
        
        negativeItem = Item(None)
        
        negativeItem.title = "Bad Title (2013) - S01E12 [ 2013 ] [ MKV | x264 | HDTV | 720p | Scene | FastTorrent ] [ Uploader: Anonymous ]  [ Bad.Title.CA.S01E12.720p.HDTV.x264-KILLERS ]"
        negativeItem.link = "http://broadcasthe.net/torrents.php?action=download&amp;authkey=ff9be6ee72a2a26d365f4454a98db5f6&amp;torrent_pass=tkfh3yf4o60c8nlyxny0x7lrqpg77k1a&amp;id=306735"
        negativeItem.description = "fareou"
#"Episode Name: Daddy Issues<br />\
#Season: 1<br />\
#Episode: 12<br />\
#Aired: 2013-09-09<br />\
#<br />\
#Episode Overview:<br />\
#When Maggie�s dad comes to town, NotJ@$0N and Mark vie for his attention but discover a secret he�s been keeping in the process. Meanwhile the new, hardworking waitress at the bar quickly becomes Maggie�s nemesis.<br />\
#<br />\
#Episode Image <br />\
#[img=https://cdn2.broadcasthe.net/tvdb/banners/episodes/269538/4630029.jpg]"
        negativeItem.rawTimestamp = "Tue, 10 Sep 2013 00:38:35 +0000"
        negativeItem.timestamp = time.strptime(negativeItem.rawTimestamp, "%a, %d %b %Y %H:%M:%S %z")
        
        return negativeItem

    def testFilter(self):
        
        
        globalContext = Bootstraper()
        globalContext.boot()
        
        app = globalContext.app
        
        configuration = app.configuration

        items = []
        
        positiveItem = self.createPositiveItem()
        negativeItem = self.createNegativeItem()
        
        items.append(positiveItem)
        items.append(negativeItem)
        
        rawConfiguration = {
                            'file': None,
                            'expression': '.*Satisfaction.*',
                            'type': 'regex',
                            'property': 'title'}
                
        testFilter = Filter(rawConfiguration, "Test Filter")
        
        filters = {testFilter}
        
        filteredItems = app.filterItems(items, filters)
        
        self.assertEqual(1, len(filteredItems), "There should be only one item left in filtered item list.")
        
        for item in filteredItems:
            
            self.assertTrue("Satisfaction" in item.title, "Title should contain one item with 'Satisfaction' in it's title.")
        
        pass
        
    def testFileFilter(self):
        
        globalContext = Bootstraper()
        globalContext.boot()
        
        app = globalContext.app

        items = []
        
        positiveItem = self.createPositiveItem()
        negativeItem = self.createNegativeItem()
        
        positiveItemSecondCriteria = copy.copy(positiveItem)
        positiveItemSecondCriteria.title = "MagicString - 123 - face.mcfh"
        
        items.append(positiveItem)
        items.append(positiveItemSecondCriteria)
        items.append(negativeItem)
        
        rawConfiguration = {
                            'file': 'filter.txt',
                            'type': 'regex',
                            'property': 'title'}
                
        testFilter = Filter(rawConfiguration, "Test Filter")
        
        filters = {testFilter}
        
        filteredItems = app.filterItems(items, filters)
        
        self.assertEqual(2, len(filteredItems), "There should be two items left in filtered item list.")
        
        for item in filteredItems:
            
            self.assertTrue("Satisfaction" in item.title or "MagicString" in item.title, "Title should contain one item with 'Satisfaction' in it's title.")
        
        
    def testCheckExisting(self):
        
        globalContext = Bootstraper()
        globalContext.boot()
        
        app = globalContext.app

        items = []
        
        item = self.createPositiveItem()
        
        items.append(item)
        
        otherItem = copy.copy(item)
        items.append(item)
        items.append(self.createNegativeItem())
        
        source = next(iter(app.sources.values()))
        destination = next(iter(app.destinations.values()))
        firstFilter = app.filters["nameRegex"]
    
        self.assertEqual("tv", destination.name)
        self.assertEqual(destination.name, source.defaultDestination)
        self.assertEqual(destination.name, firstFilter.destination)
        
        self.assertEqual("start.tv", source.directory)
        self.assertEqual("download.tv", destination.directory)
        
        app.sqlLiteClientFactory = MockSqlLiteClientFactory()
        
        exists = app.checkExists(item)
        
        self.assertFalse(exists, "Item shall not exist before it is marked downloaded.");
        
        app.markDownloaded(item)
        
        exists = app.checkExists(item)
        
        self.assertTrue(exists)
        
    
    def testDownloadDescriptor(self):
        
        self.assertFalse(True, "Implement me!!!!!!!!!!!!!!!!!!!!!111111111")