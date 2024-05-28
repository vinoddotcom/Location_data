import requests
import json
import time
import os
import re

# List of cities to query
cities = list(set(["Alberta", "British Columbia", "Manitoba", "New Brunswick", "Newfoundland and Labrador", "Nova Scotia", "Ontario", "Prince Edward Island", "Quebec", "Saskatchewan", "Northwest Territories", "Nunavut", "Yukon"]))


# Base URL for the Nominatim API
base_url = "https://nominatim.openstreetmap.org/search?addressdetails=1&format=jsonv2&limit=1&addressdetails=1&extratags=1&accept-language=en"

country_name = "Japan"

# Checkpoint file to save progress
checkpoint_file = f"{country_name}_data_checkpoint.json"

# Function to get city data from the API
def get_city_data(city, country=country_name, isfeatureType=True):
  city = re.sub(r'\(.*?\)', '', city)
  if isfeatureType:
    url = f"{base_url}&featureType=settlement&q={city} {country}"
  else:
    url = f"{base_url}&q={city} {country}"
  
  headers = {
    'User-Agent': 'DF/1.0 (bapami8521@lucvu.com)' # Replace with your email and app details
  }
  
  response = requests.get(url, headers=headers)
  if response.status_code == 200:
    res = response.json()
    if res:
      return res
    elif isfeatureType:
      print(f"Fallback: {city}")
      return get_city_data(city, country=country_name, isfeatureType=False)
    else:
      return res
  else:
    print(f"Error fetching data for {city}: {response.status_code}")
    print(response.content)
    return []

# Load previous results if checkpoint file exists
if os.path.exists(checkpoint_file):
  with open(checkpoint_file, "r", encoding="utf-8") as f:
    results = json.load(f)
else:
  results = {}

# Fetch data for each city and extract the required properties
for city in cities:
  if city in results:
    print(f"Skipping {city} (already processed)")
    continue

  time.sleep(1)
  city_data = get_city_data(city)
  if city_data:
    first_result = city_data[0]
    display_name = first_result.get("display_name", "")
    place_id = first_result.get("place_id", "")
    results[city] = {
      "display_name": display_name,
      "place_id": place_id
    }
  else:
    results[city] = {
      "display_name": "Not found",
      "place_id": "Not found"
    }
    print(f"Not found: {city}")
  
  # Save progress to checkpoint file
  with open(checkpoint_file, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=4)
  
  print(city)

# Save the final results to a JSON file
with open(f"data/{country_name}_data_v_1.json", "w", encoding="utf-8") as f:
  json.dump(results, f, ensure_ascii=False, indent=4)

print(f"Data saved to {country_name}_data_v_1.json")