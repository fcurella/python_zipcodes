import os
from StringIO import StringIO
import pickle
import sqlite3
from python_zipcodes.exceptions import ImproperlyConfiguredError

class DummyStorage(object):
    def __init__(self, *args, **kwargs):
        try:
            self.importer = kwargs['importer']
            self.fill_cache()
        except KeyError:
            raise ImproperlyConfiguredError

    def fill_cache(self):
        self.cached_data = self.read()

    def read(self):
        try:
            content = open(os.path.join(self.importer.cache_dir, self.importer.txt), 'rb')
        except IOError:
            content = self.importer.download()
        content.seek(0)
        return self.importer.parse(content)

    def update(self):
        self.cached_data = self.importer.parse(self.importer.download())

    def save(self, zip_codes):
        pass

    def compile(self):
        content = open(os.path.join(self.importer.cache_dir,self.importer.txt), 'rb')
        zip_codes = self.importer.parse(content)
        content.close()
        self.save(zip_codes)
        return zip_codes


class PickleStorage(DummyStorage):
    pickled = 'zipcodes.pickled'

    def read(self):
        try:
            f = open(os.path.join(self.importer.cache_dir, self.pickled, 'rb'))
            zip_codes = pickle.load(f)
            f.close()
            return zip_codes
        except IOError:
            return self.compile()
    
    def save(self, zip_codes):
        f = open(os.path.join(self.importer.cache_dir, self.pickled), 'wb')
        pickle.dump(zip_codes, f)
        f.close()


class SqliteStorage(DummyStorage):
    db = 'zipcodes.db'

    def fill_cache(self):
        self.conn = sqlite3.connect(os.path.join(self.importer.cache_dir, self.db))
        self.conn.row_factory = sqlite3.Row
        try:
            super(SqliteStorage, self).fill_cache()
        except sqlite3.OperationalError:
            self.cached_data = self.compile()
            self.save(self.cached_data)

    def read(self):
        c = self.conn.cursor()
        zipcodes = {}
        c.execute('select * from zipcodes')
        for r in c:
            zipcodes[r['zipcode']] = {'city':r['city'], 'state':r['state']}
        c.close()
        return zipcodes

    def save(self, zip_codes):
        c = self.conn.cursor()
        c.execute("""drop table if exists zipcodes""")
        c.execute("""create table zipcodes
(zipcode text, city text, state text)""")
        self.conn.commit()
        for k, r in zip_codes.items():
            c.execute('insert into zipcodes values (?,?,?)', [k, r['city'], r['state']])
        self.conn.commit()
        c.close()

class DjangoStorage(DummyStorage):
    def read(self):
        zipcodes = ZipCode.objects.filter(country=self.importer.country)
        zip_dict = {}
        for z in zipcodes:
            zip_dict[z.zipcode] = {'city':z.city, 'state':z.state}
        return zip_dict

    def save(self, zipcodes):
        ZipCode.objects.all().delete()
        for k, r in zip_codes.items():
            ZipCode.objects.create(zipcode=k, city=r['city'], state=r['state'])

class DjangoStorage(DummyStorage):
    def __init__(self, *args, **kwargs):
        super(DjangoStorage, self).__init__(*args, **kwargs)
        try:
            self.model = kwargs['model']
        except KeyError:
            raise ImproperlyConfiguredError

    def read(self):
        zipcodes = self.model.objects.filter(country=self.importer.country)
        zip_dict = {}
        for z in zipcodes:
            zip_dict[z.zipcode] = {'city':z.city, 'state':z.state}
        return zip_dict

    def save(self, zipcodes):
        self.model.objects.filter(country=self.importer.country).delete()
        for k, r in zip_codes.items():
            self.model.objects.create(zipcode=k, city=r['city'], state=r['state'], country=self.importer.country)
