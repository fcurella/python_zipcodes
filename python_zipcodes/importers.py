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
        self.cache_dir = os.path.join(os.path.dirname(__file__),'countries', self.country)

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
    def __init__(self, storage=DummyStorage, storage_args={}, *args, **kwargs):
        self.storage = storage
        self.storage_args = storage_args
        self.cache_codes = {}
        self.importers = {}

    def add(self, country):
        country_name = country.lower()
        module_name = 'python_zipcodes.countries.%s.importer' % country_name
        importer = __import__(module_name, globals(), locals(), ['importer',], -1)
        self.importers[country_name] = importer.Importer(storage=self.storage, storage_args=self.storage_args)


    def get(self, country):
        country_name = country.lower()
        try:
            return self.importers[country_name]
        except KeyError:
            self.add(country_name)
            return self.get(country_name)
    
    def zipcodes(self, country):
        country_name = country.lower()
        try:
            return self.importers[country_name].zipcodes()
        except KeyError:
            self.add(country_name)
            return self.zipcodes(country_name)
    
    def find(self, country, zipcode):
        country_name = country.lower()
        try:
            return self.importers[country_name][zipcode]
        except KeyError:
            self.add(country_name)
            return self.find(country_name, zipcode)
        
        def update(self, country):
        country_name = country.lower()
        try:
            return self.importers[country_name].update()
        except KeyError:
            self.add(country_name)
            return self.update(country_name)

        

