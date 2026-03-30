"""List all available stations uing icoscp python lib"""
from icoscp.station import station

station_list = station.getIdList()  # Returns a Pandas DataFrame.
for item in station_list.itertuples():
    print(item)

station_list.to_csv("output/0.icoscp_stations.csv")

# station_list = station.getIdList()  # Returns a Pandas DataFrame.
# for item in station_list.itertuples():
#     x = station.get(item.id)
#     print(x)

