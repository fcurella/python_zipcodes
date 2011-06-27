import pickle
import httplib2

class ImproperlyConfiguredError(Exception):
    pass

class GenericImporter(object):
        
    url = 'http://www.census.gov/tiger/tms/gazetteer/zips.txt'
    txt = 'zipcodes.txt'
    pickled = 'zipcodes.pickled'

    def __init__(self, *args, **kwargs):
        if self.url is None:
            raise ImproperlyConfiguredError

    def download(self):
        client = httplib2.Http()
        resp, content = client.request(self.url)
        f = open(self.txt, 'wb')
        f.write(content).close()
        return content
    
    def parse(self, content):
        raise NotImplementedError

    def build_dict():
        try:
            content = open(self.txt, 'rb')
        except IOError:
            content = self.download()

        return self.parse(content)

    def zipcodes():
        try:
            records = pickle.load(open(self.pickled, 'rb'))
        except IOError:
            records = self.build_dict()
            pickle.dump(records, open(self.pickled, 'wb'))
        return records

class ZipCode(object):
    def __init__(self, country, *args, **kwargs):
        module_name = 'python_zipcodes.countries.%s.importer' % country
        importer = __import__(module_name)
        c = importer.Importer()
        return c.zipcodes()