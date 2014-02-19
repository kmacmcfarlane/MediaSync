import time


class Item(object):
    
    def __init__(self, itemElement):
        
        if itemElement is not None:
            self.title = itemElement.find('title').text
            self.link = itemElement.find('link').text
            self.description = itemElement.find('description').text
            self.rawTimestamp = itemElement.find('pubDate').text
            self.timestamp = time.strptime(self.rawTimestamp, "%a, %d %b %Y %H:%M:%S %z")
        else:
            self.title = None;
            self.link = None;
            self.description = None;
            self.description = None;
            self.rawTimestamp = None;
            self.timestamp = None;