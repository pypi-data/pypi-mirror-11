======
README
======

This package provides a geo locaiton database supporting longitude/latitude,
country, city and timezone lookup based on the MaxMind geo location database.

  >>> import sys
  >>> import os.path
  >>> import p01.geo.locator

  >>> path = os.path.join(os.path.dirname(p01.geo.__file__), 'data')
  >>> db = os.path.join(path, 'GeoLite2-City.mmdb')
  >>> locator = p01.geo.locator.GeoLocator(db)
  >>> locator
  <p01.geo.locator.GeoLocator object at ...>


The locator provides a generic API where we can get all data based on a given
IP adress:

  >>> ip = '86.101.28.131'
  >>> data = locator.getData(ip)
  >>> data
  <GeoData for 86.101.28.131>

  >>> data.countryCode
  u'HU'

  >>> data.countryName
  u'Hungary'

  >>> data.metroCode is None
  True

  >>> data.city is None
  True

  >>> data.cityGeoName is None
  True

  >>> data.timezone
  <DstTzInfo 'Europe/Budapest' LMT+1:16:00 STD>

  >>> data.longitude
  19.0514

  >>> data.latitude
  47.4925

  >>> data.postalCode is None
  True

Looking up a timezone based on IP is faster and consumes less RAM for caching:

  >>> tz = locator.getTimeZone(ip)
  >>> tz
  <DstTzInfo 'Europe/Budapest' LMT+1:16:00 STD>

As you can see the teimzone can we get with the zone property (non unicode):

  >>> tz.zone
  'Europe/Budapest'

Not all IPs are present:

  >>> ip = '254.254.254.254'
  >>> locator.getData(ip)

  >>> locator.getTimeZone(ip) is None
  True

We get exceptions on bad IPs:

  >>> ip = '86.101.28.13x'
  >>> locator.getData(ip) is None
  True

  >>> locator.getTimeZone(ip) is None
  True

We can get a locator that loads the db and tzdb and stays around
in a global variable:

  >>> from p01.geo.locator import get_loaded_locator
  >>> locator = get_loaded_locator()

This locator will work just like normal

  >>> ip = '217.10.9.34'
  >>> locator.getData(ip)
  <GeoData for 217.10.9.34>

Running get_loaded_locator will get us the same locator again,
there is no fresh delay to load the db and tzdb:

  >>> locator2 = get_loaded_locator()
  >>> locator is locator2
  True

We can override the paths for the db and tzdb when loading the locator:

  >>> path = os.path.join(os.path.dirname(p01.geo.__file__), 'data')
  >>> db = os.path.join(path, 'GeoLite2-City.mmdb')
  >>> tzdb = os.path.join(path, 'timezone.txt')
  >>> paths = {'db':db, 'tzdb':tzdb}
  >>> locator = get_loaded_locator(paths)
  >>> locator
  <p01.geo.locator.GeoLocator object at ...>


Test an IP wit more data:

  >>> ip = '128.101.101.101'
  >>> obj = locator.getData(ip)
  >>> obj
  <GeoData for 128.101.101.101>

  >>> obj.ip
  '128.101.101.101'

  >>> obj.countryCode
  u'US'

  >>> obj.countryName
  u'United States'

  >>> obj.countryGeoName
  6252001

  >>> obj.metroCode
  613

  >>> obj.city
  u'Minneapolis'

  >>> obj.cityGeoName
  5037649

  >>> obj.timezone
  <DstTzInfo 'America/Chicago' LMT-1 day, 18:09:00 STD>

  >>> obj.longitude
  -93.2166

  >>> obj.latitude
  44.9759

  >>> obj.postalCode
  u'55414'


MaxItemCache
------------

Our thread local storage with max item invalidation is not much slower:

  >>> cache = p01.geo.locator.MaxItemCache(maxitems=100000)
  >>> locator = p01.geo.locator.GeoLocator(db, cache=cache)

Test an IP wit more data:

  >>> ip = '128.101.101.101'
  >>> obj = locator.getData(ip)
  >>> obj
  <GeoData for 128.101.101.101>

  >>> obj.ip
  '128.101.101.101'

  >>> obj.countryCode
  u'US'

  >>> obj.countryName
  u'United States'

  >>> obj.countryGeoName
  6252001

  >>> obj.metroCode
  613

  >>> obj.city
  u'Minneapolis'

  >>> obj.cityGeoName
  5037649

  >>> obj.timezone
  <DstTzInfo 'America/Chicago' LMT-1 day, 18:09:00 STD>

  >>> obj.longitude
  -93.2166

  >>> obj.latitude
  44.9759

  >>> obj.postalCode
  u'55414'

One item has the size in ram:

  >>> sys.getsizeof(obj)
  76
