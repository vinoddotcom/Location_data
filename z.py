import json

with open("res_output_data.json", 'r') as f:
    map = json.load(f)


allLocations = {}
for key, item in map.items():
    arr = []
    for loc in item.values():
        details = {}
        details["osm_id"] = loc.get("osm_id")
        details["description"]  = loc.get("description")
        arr.extend([details])
    allLocations[key] = arr

with open("alert_locations.json", 'w') as f:
    json.dump(allLocations, f, ensure_ascii=False)

