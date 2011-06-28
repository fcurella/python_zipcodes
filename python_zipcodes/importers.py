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
        if not self.cached_data:
            self.cached_data = self._read_from_db()
        return self.cached_data
    
    def _read_from_db(self):
        c = self.conn.cursor()
        zipcodes = {}
        try:
            c.execute('select * from zipcodes')
            for r in c:
                zipcodes[r['zipcode']] = {'city':r['city'], 'state':r['state']}
        except sqlite3.OperationalError:
            print "rebuilding db"
            zipcodes = self.build_dict()
            c.execute("""drop table if exists zipcodes""")
            c.execute("""create table zipcodes
(zipcode text, city text, state text)""")
            self.conn.commit()
            for k, r in self.cache_data.items():
                c.execute('insert into zipcodes values (?,?,?)', [k, r['city'], r['state']])
            self.conn.commit()
        c.close()
        return zipcodes
        
    def __getitem__(self, key):
        if not self.cached_data:
            self.cached_data = self.zipcodes()
        return self.cached_data[key]

    def get(self, key):
        sql = """SELECT * FROM zipcodes WHERE zipcode = ?"""
        c = self.conn.cursor()
        c.execute(sql, [key])
        rows = list(c)
        if len(rows):
            return {'city': rows[0]['city'], 'state':rows[0]['state']}
        return KeyError


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

