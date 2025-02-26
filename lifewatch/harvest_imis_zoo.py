import urllib.request
import json
from pprint import pprint

zooplankton_url = "https://www.vliz.be/nl/imis?module=dataset&dasid=4687&show=json"

with urllib.request.urlopen(zooplankton_url) as url:
    data = json.load(url)
    # pprint(data)

with open('../oceanOps_template.json') as json_file:
    ocean_ops = json.load(json_file)
    pprint(ocean_ops)

title = json.dumps(data["datasetrec"]["StandardTitle"])
owner_surname = json.dumps(data["ownerships"][0]["Surname"])
owner_firstname = json.dumps(data["ownerships"][0]["Firstname"])
owner_email = json.dumps(data["ownerships"][0]["Email"])
start_date = json.dumps(data["temporal"][0]["StartDate"])
end_date = json.dumps(data["temporal"][0]["EndDate"])

print(title)
print(owner_surname)
print(owner_firstname)
print(owner_email)
print(start_date)
print(end_date)


geo = data["geographical"]
print(geo)
for i in range(len(geo)):
    print("station ", json.dumps(geo[i]["StationName"]))
    print("x: ", json.dumps(geo[i]["OrigCoordMinX"]))
    print("y: ", json.dumps(geo[i]["OrigCoordMinY"]))


# ocean_ops["identification"]["platform_description"] = title
# ocean_ops["operation"]["deploy_date"] = start_date
# pprint(ocean_ops)

