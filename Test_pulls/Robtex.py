from geoip import geolite2

match = geolite2.lookup('17.0.0.1')
print match

print match.country
print match.subdivisions
print match.timezone