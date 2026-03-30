# ICOS

## ICOS stations
List of stations can be obtained, demonstrated in  ```0.search_icoscp_stations.py```.
List can be filtered on 
- name: "Thornton Buoy"
- stationTheme: "http://meta.icos-cp.eu/ontologies/cpmeta/OS" for oceanic stations.
- siteType: "fixed stations" for fixed stations (vs SOOP for cruises)

### Station: Thornton buoy
Station information can be found via uri in stations list. 
For Thornton buoy, this is https://meta.icos-cp.eu/resources/stations/OS_1199. 

Demonstrated in ```1.search_icoscp_thornton.py```. 
The station contains basic information. 
```
{
 "stationId": "BE-FOS-Thornton Buoy",
 "name": "Thornton Buoy",
 "theme": "OS",
 "icosclass": "1",
 "siteType": "fixed station",
 "lat": 51.57989,
 "lon": 2.993217,
 "eas": null,
 "firstName": "Andre",
 "lastName": "Cattrijsse",
 "email": "andre.cattrijsse@vliz.be",
 "country": "BE",
 "project": [
  "ICOS"
 ],
 "uri": [
  "http://meta.icos-cp.eu/resources/stations/OS_1199"
 ]
}
```
#### Data releases
Each station has multiple data releases.
Demonstrated in ```2.search_meta_file.py```

The result is a json.
