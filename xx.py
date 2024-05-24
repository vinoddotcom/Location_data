import requests
import json
import time

# List of cities to query
cities = list(set([
  'Kamaishi Ishikawa',      'Higashikunisaki Ōita',
  'Kitamatsuura Nagasaki',  'Minamiuwa Ehime',
  'San Yamaguchi',          'Miyako Ishikawa',
  'Kamihei Ishikawa',       'Kunohe Ishikawa',
  'Kitakami Ishikawa',      'Rikuzentakata Ishikawa',
  'Ichinoseki Ishikawa',    'Ōchi Shimane',
  'Hachimantai Ishikawa',   'Shimohei Ishikawa',
  'Tōno Ishikawa',          'Higashimatsuura Saga',
  'Kitaazumi Nagano',       'Waga Ishikawa',
  'Nishisonogi Nagasaki',   'Nishimatsuura Saga',
  'Kan Kagawa',             'Sanbu Chiba',
  'Kitauwa Ehime',          'Ōfunato Ishikawa',
  'Kita Ehime',             'Shiwa Ishikawa',
  'Isawa Ishikawa',         'Ninohe Ishikawa',
  'Toyota Hiroshima',       'Nan Yamagata',
  'Higashisonogi Nagasaki', 'Hōsu Ishikawa',
  'Santō Niigata',          'Kesen Ishikawa',
  'Morioka Ishikawa',       'Kamiina Nagano',
  'Takizawa Ishikawa',      'Hanamaki Ishikawa',
  'Kuji Ishikawa',          'Mo Tochigi',
  'Nishiiwai Ishikawa',     'Ōshima Kagoshima'
]))

# Base URL for the Nominatim API
base_url = "https://nominatim.openstreetmap.org/search?addressdetails=1&format=jsonv2&limit=1&addressdetails=1&extratags=1&accept-language=en"

# Function to get city data from the API
def get_city_data(city, country="Japan",isfeatureType=True):
    city = city.split()[0]
    if isfeatureType: url = f"{base_url}&featureType=settlement&q={city} {country}"
    else: url = f"{base_url}&q={city} {country}"
    print(url)
    headers = {
        'User-Agent': 'DF/1.0 (bapami8521@lucvu.com)'  # Replace with your email and app details
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        res = response.json()
        if res: return res
        elif isfeatureType: 
            print(f"Follback: {city}")
            return get_city_data(city, country="Japan", isfeatureType=False)
        else: return res
    else:
        print(f"Error fetching data for {city}: {response.status_code}")
        print(response.content)
        return []

# Dictionary to hold the results
results = {}

# Fetch data for each city and extract the required properties
for city in cities:
    time.sleep(1)
    city_data = get_city_data(city)
    if city_data:
        # Assuming we take the first result if there are multiple
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
        print(f"not found {city}")
    print(city)

# Save the results to a JSON file
with open("Canada_data_v_1.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=4)

print("Data saved to Canada_data.json")
