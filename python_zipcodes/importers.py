import pickle
import httplib2
import os
from StringIO import StringIO

class ImproperlyConfiguredError(Exception):
    pass

class GenericImporter(object):
        
    url = None
    country = None
    txt = 'zipcodes.txt'
    pickled = 'zipcodes.pickled'

    def __init__(self, *args, **kwargs):
        if self.url is None:
            raise ImproperlyConfiguredError
        if self.country is None:
            raise ImproperlyConfiguredError
        self.cache_dir = os.path.join('python_zipcodes','countries', self.country)

    def download(self):
        client = httplib2.Http()
        resp, content = client.request(self.url)
        f = open(os.path.join(self.cache_dir,self.txt), 'wb')
        f.write(content)
        f.close()
        return StringIO(content)
    
    def update(self):
        self.download()
        self.zipcodes()

    def parse(self, content):
        raise NotImplementedError

    def build_dict(self):
        try:
            content = open(self.txt, 'rb')
        except IOError:
            content = self.download()
        content.seek(0)
        return self.parse(content)

    def zipcodes(self):
        try:
            records = pickle.load(open(os.path.join(self.cache_dir,self.pickled), 'rb'))
        except IOError:
            records = self.build_dict()
            pickle.dump(records, open(os.path.join(self.cache_dir,self.pickled), 'wb'))
        return records

class ZipCodeManager(object):
    def __init__(self, *args, **kwargs):
        self.cache_codes = {}

    def get(self, country):
        try:
            return self.cache_codes[country.lower()]
        except KeyError:
            module_name = 'python_zipcodes.countries.%s.importer' % country.lower()
            importer = __import__(module_name, globals(), locals(), ['importer',], -1)
            c = importer.Importer()
            zipcodes = c.zipcodes()
            self.cache_codes[country.lower()] = zipcodes 
            return zipcodes

