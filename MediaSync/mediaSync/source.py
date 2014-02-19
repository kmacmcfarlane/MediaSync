class Source(object):
    
    def __init__(self, sourceConfiguration, name):
        self.name = name
        self.uri = sourceConfiguration["uri"]
        self.directory = sourceConfiguration["directory"]
        self.filters = sourceConfiguration["filters"]
        self.destinationName = sourceConfiguration["destinationName"]