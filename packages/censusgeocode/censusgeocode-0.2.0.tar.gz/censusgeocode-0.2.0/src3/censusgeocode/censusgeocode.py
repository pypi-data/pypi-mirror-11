#!/usr/local/bin/python3

"""
Census Geocoder wrapper
see http://geocoding.geo.census.gov/geocoder/Geocoding_Services_API.pdf
Accepts either named `lat` and `lng` or x and y inputs.
"""

from urllib import parse, request
from urllib.error import URLError, HTTPError
import json

GEOGRAPHYVINTAGES = ['Current', 'ACS2014', 'ACS2013', 'ACS2012', 'Census2010', 'Census2000']
BENCHMARKS = ['Public_AR_Current', 'Public_AR_ACS2014', 'Public_AR_Census2010']


class CensusGeocode(object):
    '''Fetch results from the Census Geocoder'''
    # pylint: disable=R0921

    _url = "http://geocoding.geo.census.gov/geocoder/{returntype}/{searchtype}"
    returntypes = ['geographies', 'locations']

    def __init__(self, benchmark=None, geovintage=None):
        '''
        benchmark -- A name that references the version of the locator to use. See http://geocoding.geo.census.gov/geocoder/benchmarks
        geovintage -- The geography part of the desired vintage. For instance, for the vintage 'ACS2014_Current':
        >>> CensusGeocode(benchmark='Current', geovintage='ACS_2014')
        See http://geocoding.geo.census.gov/geocoder/vintages?form
        '''
        self.benchmark = benchmark or BENCHMARKS[0]
        geographyvintage = geovintage or GEOGRAPHYVINTAGES[0]

        self.vintage = geographyvintage + self.benchmark.replace('Public_AR', '')

    def _geturl(self, searchtype, returntype=None):
        returntype = returntype or self.returntypes[0]
        return self._url.format(returntype=returntype, searchtype=searchtype)

    def _fetch(self, searchtype, fields, layers=None, returntype=None):
        fields['vintage'] = self.vintage
        fields['benchmark'] = self.benchmark
        fields['format'] = 'json'

        if layers:
            fields['layers'] = layers

        returntype = returntype or 'geographies'

        url = self._geturl(searchtype, returntype) + '?' + parse.urlencode(fields)

        try:
            response = request.urlopen(url)
            return CensusResult(json.loads(response.read().decode('utf-8')))

        except HTTPError as e:
            raise e

        except URLError as e:
            raise e

    def coordinates(self, x, y, layers=None, returntype=None):
        '''Geocode a (lon, lat) coordinate.'''
        fields = {
            'x': x,
            'y': y
        }

        return self._fetch('coordinates', fields, layers, returntype)

    def address(self, street, city=None, state=None, zipcode=None, layers=None, returntype=None):
        '''Geocode an address.'''
        fields = {
            'street': street,
            'city': city,
            'state': state,
            'zip': zipcode,
        }

        return self._fetch('address', fields, layers, returntype)

    def onelineaddress(self, address, layers=None, returntype=None):
        '''Geocode an an address passed as one string.
        e.g. "4600 Silver Hill Rd, Suitland, MD 20746"
        '''

        fields = {
            'address': address,
        }

        return self._fetch('onelineaddress', fields, layers, returntype)

    def addressbatch(self, data, returntype=None):
        raise NotImplementedError


class CensusResult(list):

    def __init__(self, data):
        self.input = data['result']['input']

        try:
            super(CensusResult, self).__init__(data['result']['addressMatches'])

        except KeyError:
            super(CensusResult, self).__init__([data['result']['geographies']])

