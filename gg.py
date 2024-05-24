import requests
from xml.etree import ElementTree

# Define the Overpass API endpoint
url = "http://overpass-api.de/api/interpreter"

# Define the Overpass query to get all districts in Japan in English, including place IDs
query = """
[out:xml];
area["ISO3166-1"="JP"][admin_level=2];
(node["place"="city"]["name:en"](area);
 way["place"="city"]["name:en"](area);
 rel["place"="city"]["name:en"](area);
);
out body;
"""

# Send the query to the Overpass API
response = requests.post(url, data={'data': query})

# Check if the request was successful
if response.status_code == 200:
    # Parse the XML response
    root = ElementTree.fromstring(response.content)

    # Extract district names in English and their IDs
    districts = []
    for element in root.findall('.//tag[@k="name:en"]/..'):
        name_en = element.find('./tag[@k="name:en"]').get('v')
        place_id = element.get('id')
        districts.append((name_en, place_id))

    # Print the district names in English and their IDs
    for name_en, place_id in districts:
        print(f"Name: {name_en}, Place ID: {place_id}")
else:
    print("Failed to retrieve data:", response.status_code)
