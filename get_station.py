from icoscp.station import station
my_station = station.get('BE-FOS-Thornton Buoy')

for key, value in my_station.info().items():
    print(key, " - ",  value)



