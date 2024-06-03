import json
import time
import requests

with open("new_map.json", 'r') as f:
    map = json.load(f)

with open("field_val_with_lat_long.json", 'r') as f:
    field_val_with_lat_long = json.load(f)

with open("res_output_data.json", 'r') as f:
    new_data_with_res = json.load(f)


allLocations = []
for item in new_data_with_res.values():
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


for key, item in map.items():
    is_matched = get_nested_value(item, ["match"])
    if is_matched: continue

    lat = get_nested_value(field_val_with_lat_long, [key, "lat"])
    long = get_nested_value(field_val_with_lat_long, [key, "long"])

    if not lat or not long:
        print(f"not found lat: {lat}, long: {long}, key: {key}")

    base_url = "https://nominatim.openstreetmap.org/reverse?format=json&zoom=18&addressdetails=1&accept-language=en&extratags=1"
    time.sleep(1)
    url = f"{base_url}&&lat={lat}&lon={long}"
  
    headers = {
      'User-Agent': 'DF/1.0 (bapami8521@lucvu.com)' # Replace with your email and app details
    }
  
    response = requests.get(url, headers=headers)
    res = response.json()
    if res:
        details = {}


        state = get_nested_value(res, ["address", "state"])
        state_district = get_nested_value(res, ["address", "state_district"])
        country = get_nested_value(res, ["address", "country"])

        
        if not state_district: details["state_district"] = "not found"
        if not state: details["state"] = "not found"
        if not country: details["country"] = "not found"

        print(state_district, state, country)
        details["res"] = res
        if not state_district or not state or not country: 
            map[key] = details
            print("not found", key, details)
            print("\n\n\n\n\n")
            continue


        for place in allLocations:
            place_state = get_nested_value(place, ["res", "address", "state"])
            place_state_district = get_nested_value(place, ["res", "address", "state_district"])
            place_country = get_nested_value(place, ["res", "address", "country"])

            if not place_state or not place_state_district or not place_country: continue
            details["res"] = res
            if country == place_country and   place_state_district == state_district and place_state_district == state_district:
                details["match"] = place["osm_id"]
                print("match", key)
                map[key] = details
                print("\n\n\n\n\n")
                break
        map[key] = details
    else: print(f"res not found for url: {url}")

with open("new_new_map.json", 'w') as f:
    json.dump(map, f, indent=4, ensure_ascii=False)

