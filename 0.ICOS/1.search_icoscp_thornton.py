"""search & list all icos stations using icoscp"""
from icoscp.station import station
import json

my_station = station.get('BE-FOS-Thornton Buoy')
help(my_station)

# -----------------------------------------------------------------------------
# INFO
# -----------------------------------------------------------------------------

for key, value in my_station.info().items():
    print(key, " - ",  value)


with open('output/1.icoscp_thornton.json', 'w') as dest:
    json.dump(my_station.info(), dest, indent=1)

# -----------------------------------------------------------------------------
# PRODUCTS
# -----------------------------------------------------------------------------
products = my_station.products()
print(products)

# -----------------------------------------------------------------------------
# DATA
# -----------------------------------------------------------------------------
data = my_station.data()
for i in data.itertuples():
    print(i)

data.to_csv("output/1.icoscp_thornton_data.csv")


