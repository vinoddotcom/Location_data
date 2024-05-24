import requests
import time
import json



# Load the JSON data
with open('data.json', 'r') as file:
    data = json.load(file)

# Define the filtering function
def filter_function(item):
    return item['country_code'] == 'JP'

# Filter the array using filter and convert to a list
filtered_items = list(filter(filter_function, data))

# Your list of Japanese postal codes
postal_codes = [obj["postal_code"] for obj in filtered_items]

# Base URL for the Nomimatim API
base_url = "https://nominatim.openstreetmap.org/search"

# Function to get the location details from the API
def get_location_details(postal_code):
    params = {
        'postalcode': postal_code,
        'country': 'Japan',
        'countrycodes': 'JP',
        'format': 'json',
        'addressdetails': 1,
    }
    
    response = requests.get(base_url, params=params)
    print(response)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to extract the required details
def extract_details(location_data):
    if location_data:
        for place in location_data:
            if 'address' in place:
                address = place['address']
                return {
                    'place_id': place.get('place_id', ''),
                    'display_name': place.get('display_name', ''),
                    'district': address.get('suburb', address.get('city_district', '')),
                    'state': address.get('state', ''),
                    'country': address.get('country', ''),
                }
    return None

# Process all postal codes
location_list = []

for code in postal_codes:
    location_data = get_location_details(code)
    details = extract_details(location_data)
    if details:
        location_list.append(details)
    # Sleep for a second to avoid hitting the rate limit
    time.sleep(1)

# Print the results
for location in location_list:
    print(location)

# Optionally, save the results to a file
import json
with open('locations.json', 'w') as file:
    json.dump(location_list, file, indent=4)
