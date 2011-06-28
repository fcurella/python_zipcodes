import httplib2
import os
from StringIO import StringIO
from python_zipcodes.exceptions import ImproperlyConfiguredError
from python_zipcodes.storages import DummyStorage

class GenericImporter(object):
        
    url = None
    country = None
    txt = 'zipcodes.txt'

    def __init__(self, storage=DummyStorage, *args, **kwargs):
        if self.url is None:
            raise ImproperlyConfiguredError
        if self.country is None:
            raise ImproperlyConfiguredError
        self.cache_dir = os.path.join('python_zipcodes','countries', self.country)

        storage_args = kwargs.get('storage_args', {})
        storage_args.setdefault('importer', self)
        self.storage = storage(**storage_args)

    def download(self):
        client = httplib2.Http()
        resp, content = client.request(self.url)
        f = open(os.path.join(self.cache_dir,self.txt), 'wb')
        f.write(content)
        f.close()
        return StringIO(content)
    
    def parse(self, content):
        raise NotImplementedError

    def update(self):
        self.storage.update()

    def zipcodes(self):
        return self.storage.cached_data
    
    def __getitem__(self, key):
        if not self.storage.cached_data:
            self.storage.cached_data = self.storage.read()
        return self.storage.cached_data[key]


class ZipCodeManager(object):
    def __init__(self, storage=DummyStorage, *args, **kwargs):
        self.storage = storage
        self.cache_codes = {}

    def get(self, country):
        try:
            return self.cache_codes[country.lower()]
        except KeyError:
            module_name = 'python_zipcodes.countries.%s.importer' % country.lower()
            importer = __import__(module_name, globals(), locals(), ['importer',], -1)
            c = importer.Importer(storage=self.storage)
            zipcodes = c.zipcodes()
            self.cache_codes[country.lower()] = zipcodes 
            return zipcodes

