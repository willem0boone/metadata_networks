from icoscp.station import station
import json

my_station = station.get('BE-FOS-Thornton Buoy')

for key, value in my_station.info().items():
    print(key, " - ",  value)

print(type(my_station.info()))

with open('_thornton.json', 'w') as dest:
    json.dump(my_station.info(), dest, indent=1)


