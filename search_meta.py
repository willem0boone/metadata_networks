from icoscp.dobj import Dobj

thornton = "https://meta.icos-cp.eu/objects/sp_VuFeRlEBUcXY_LPniUWfW"
meta = "http://meta.icos-cp.eu/resources/stations/OS_1199"

dobj = Dobj(thornton)
print(type(dobj.meta))


for key, value in dobj.meta.items():
    print(key, " - ", value)
