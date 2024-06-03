import requests
import json
import os
import time


with open("final_output_data.json", 'r') as f:
    data = json.load(f)

# File paths
output_file = 'res_output_data.json'
checkpoint_file = 'checkpoint.json'

# Nominatim lookup URL
base_url = "https://nominatim.openstreetmap.org/search?addressdetails=1&format=jsonv2&limit=1&addressdetails=1&extratags=1&accept-language=en"


# Function to get Nominatim data by place_id
def get_nominatim_data(city, isfeatureType=True):
  time.sleep(1)
  if isfeatureType:
    url = f"{base_url}&featureType=settlement&q={city}"
  else:
    url = f"{base_url}&q={city}"
  
  headers = {
    'User-Agent': 'DF/1.0 (bapami8521@lucvu.com)' # Replace with your email and app details
  }
  
  response = requests.get(url, headers=headers)
  if response.status_code == 200:
    res = response.json()
    if res:
      print(city)
      return res
    elif isfeatureType:
      print(f"Fallback: {city}")
      return get_nominatim_data(city, isfeatureType=False)
    else:
      print(city)
      return res
  else:
    print(f"Error fetching data for {city}: {response.status_code}")
    print(response.content)
    return []
    
# Load checkpoint
def load_checkpoint():
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r') as f:
            return json.load(f)
    return {}

# Save checkpoint
def save_checkpoint(checkpoint):
    with open(checkpoint_file, 'w') as f:
        json.dump(checkpoint, f, ensure_ascii=False)

# Save output data
def save_output(data):
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# Check if all locations in a country are processed
def all_locations_processed(country_data, checkpoint):
    for location in country_data.keys():
        if location not in checkpoint:
            return False
    return True

# Process each location
def process_locations(data):
    checkpoint = load_checkpoint()
    counter = 0
    
    for country, locations in data.items():
        # Skip the entire country if already fully processed
        if checkpoint.get(country) == "processed":
            continue

        for location, details in locations.items():
            if checkpoint.get(country, {}).get(location):
                continue  # Skip already processed locations
            
            print(details)
            description = details['description']

            try:
                # Get Nominatim data
                nominatim_data = get_nominatim_data(description)

                if nominatim_data:
                    nominatim_info = nominatim_data[0]
                    details["res"] = nominatim_info

                    # Mark location as processed
                    if country not in checkpoint:
                        checkpoint[country] = {}
                    checkpoint[country][location] = True

                    # Save checkpoint every 20 items
                    counter += 1
                    if counter % 20 == 0:
                        save_checkpoint(checkpoint)
                        save_output(data)

            except Exception as e:
                print(f"Error processing {location} in {country}: {e}")
                save_checkpoint(checkpoint)
                save_output(data)
                raise
        
        checkpoint[country] = "processed"
        save_checkpoint(checkpoint)
        save_output(data)

    # Save remaining data and checkpoint if counter is not zero
    if counter % 20 != 0:
        save_checkpoint(checkpoint)
        save_output(data)

# Start processing
process_locations(data)

# for country, locations in data.items():
#         # Skip the entire country if already fully processed

#         for location, details in locations.items():
#             if not "osm_id" in details: 
#                 print(details)
