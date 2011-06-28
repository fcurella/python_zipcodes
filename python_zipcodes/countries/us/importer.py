from csv import reader
import pickle
import httplib2
from python_zipcodes.importers import GenericImporter

class Importer(GenericImporter):
    url = 'http://www.census.gov/tiger/tms/gazetteer/zips.txt'
    country = 'us'
    
    def parse(self, content):
        rows = reader(content, delimiter=',', quotechar='"')
        records = {}
        for r in rows:
            zipcode = r[1]
            city = r[3].title()
            state = r[2].upper()
            records.setdefault(zipcode, {'city':city, 'state':state})
        return records
