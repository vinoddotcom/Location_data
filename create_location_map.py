import json

# Load input data
with open("res_output_data.json", 'r') as f:
    new_data = json.load(f)

with open("field_values_Location_output_data.json", 'r') as f:
    old_data = json.load(f)


location_map = {}


allLocations = []
for item in new_data.values():
    allLocations.extend(item.values())

def get_nested_value(container, keys):
    for key in keys:
        if isinstance(container, dict):
            container = container.get(key)
        elif isinstance(container, list) and isinstance(key, int) and 0 <= key < len(container):
            container = container[key]
        else:
            return None
        if container is None:
            return None
    return container

for item in old_data.values():
    details = {}
    id = item["id"]
    state = get_nested_value(item, ["res", 0, "address", "state"])
    state_district = get_nested_value(item, ["res", 0, "address", "state_district"])
    country = get_nested_value(item, ["res",0, "address", "country"])

    if not state_district: details["state_district"] = "not found"
    if not state: details["state"] = "not found"
    if not country: details["country"] = "not found"

    if not state_district or not state or not country: 
        location_map[id] = details
        continue

    for place in allLocations:
        place_state = get_nested_value(place, ["res", "address", "state"])
        place_state_district = get_nested_value(place, ["res", "address", "state_district"])
        place_country = get_nested_value(place, ["res", "address", "country"])

        if not place_state or not place_state_district or not place_country: continue

        if country == place_country and   place_state_district == state_district and place_state_district == state_district:
            details["match"] = place["osm_id"]
            break
    location_map[id] = details

with open("map.json", 'w') as f:
    json.dump(location_map, f, indent=4, ensure_ascii=False)