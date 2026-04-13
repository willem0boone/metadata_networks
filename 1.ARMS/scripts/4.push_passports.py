from OceanOpsClient import OceanOpsClient
from pprint import pprint

client = OceanOpsClient()
test = client.validate_passport_json("../passports/ETN_12734_WIGOS_NONE.json")

pprint(test)

