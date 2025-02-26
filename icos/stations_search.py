"""List all available stations"""
from icoscp.station import station

station_list = station.getIdList()  # Returns a Pandas DataFrame.
for item in station_list.itertuples():
    print(item)

station_list.to_csv("stations.csv")
