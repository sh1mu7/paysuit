import json
import os

from ....models import Country, Document

GEO_DATA = "data/countries.json"


# Opening JSON file
def load_json(name):
    f = open(os.path.join(os.path.dirname(os.path.dirname(__file__)), name, ), encoding="utf8")
    data = json.load(f)
    f.close()
    return data


def load_geo_json():
    if Country.objects.count() <= 0:
        countries_json = load_json(GEO_DATA)
        countries = []
        for data in countries_json:
            country = Country(
                name=data['name'],
                code=data['isoCode'],
                phone_code=data['dialCode'],
                flag=data['flag']
            )
            countries.append(country)
        Country.objects.bulk_create(countries)
