import json
from icoscp.dobj import Dobj
from icoscp.station import station
import pandas as pd
from pprint import pprint

# -----------------------------------------------------------------------------
# get dataset json of most recent level 2 release
# -----------------------------------------------------------------------------
my_station = station.get('BE-FOS-Thornton Buoy')
data = my_station.data()
data['timeStart'] = pd.to_datetime(data['timeStart'], errors='coerce')
data_filtered = data[data["datalevel"].astype(str) == "2"]
data_filtered = data_filtered.dropna(subset=['timeStart'])
latest_record = data_filtered.loc[data_filtered['timeStart'].idxmax()]

print("latest release:")
print(latest_record)
print("-"*50)
# -----------------------------------------------------------------------------
# get dataset json of most recent level 2 release
# -----------------------------------------------------------------------------

dobj = Dobj(latest_record.dobj)

for key, value in dobj.meta.items():
    print(key, " - ", value)

print("-"*25)
pprint(dobj.meta)


with open('output/2.icoscp_thornton_latest_release.json', 'w') as dest:
    json.dump(dobj.meta, dest, indent=1)



