import httplib2
import sqlite3
import os
from StringIO import StringIO

class ImproperlyConfiguredError(Exception):
    pass


class GenericImporter(object):
        
    url = None
    country = None
    txt = 'zipcodes.txt'
    db = 'zipcodes.db'

    def __init__(self, *args, **kwargs):
        if self.url is None:
            raise ImproperlyConfiguredError
        if self.country is None:
            raise ImproperlyConfiguredError
        self.cache_dir = os.path.join('python_zipcodes','countries', self.country)
        self.cached_data = {}
        self.conn = sqlite3.connect(os.path.join(self.cache_dir,self.db))
        self.conn.row_factory = sqlite3.Row

    def download(self):
        client = httplib2.Http()
        resp, content = client.request(self.url)
        f = open(os.path.join(self.cache_dir,self.txt), 'wb')
        f.write(content)
        f.close()
        return StringIO(content)
    
    def update(self):
        self.cached_data = self.parse(self.download())
        self._write_to_db()

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
        if not self.cached_data:
            try:
                self.cached_data = self._read_from_db()
            except sqlite3.OperationalError:
                self.conn.close()
                self.cached_data = self.build_dict()
                self._write_to_db()
        return self.cached_data
    
    def _read_from_db(self):
        c = self.conn.cursor()
        zipcodes = {}
        c.execute('select * from zipcodes')
        for r in c:
            zipcodes[r['zipcode']] = {'city':r['city'], 'state':r['state']}
        c.close()
        return zipcodes
    
    def _write_to_db(self):
        c = self.conn.cursor()
        c.execute("""drop table if exists zipcodes""")
        c.execute("""create table zipcodes
(zipcode text, city text, state text)""")
        self.conn.commit()
        for k, r in self.cached_data.items():
            c.execute('insert into zipcodes values (?,?,?)', [k, r['city'], r['state']])
        self.conn.commit()
        c.close()

    def __getitem__(self, key):
        if not self.cached_data:
            self.cached_data = self.zipcodes()
        return self.cached_data[key]

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

