import overpy
import json
from decimal import Decimal

def get_districts_across_levels_and_save_to_json(japan):
    # Initialize Overpass API object
    api = overpy.Overpass()

    # Corrected Overpass query to fetch city names in English across different admin levels
    query = """
            [out:json];
            area["ISO3166-1"="JP"]->.country;

            (
              area[admin_level=2](area.country)->.a;
              (
                node["place"="city"]["name:en"](area.a);
                way["place"="city"]["name:en"](area.a);
                rel["place"="city"]["name:en"](area.a);
              );
              >;

              area[admin_level=3](area.country)->.b;
              (
                node["place"="city"]["name:en"](area.b);
                way["place"="city"]["name:en"](area.b);
                rel["place"="city"]["name:en"](area.b);
              );
              >;

            );
            out body;
    """

    districts = []

    try:
        # Execute the query
        result = api.query(query)
        
        # Extract and append the required details to the list
        for element in result.nodes + result.ways + result.relations:
            if "name:en" in element.tags:
                place_type = element.tags.get("place", "unknown")
                display_name = f"{element.tags['name:en']}, {place_type}"
                # Convert Decimal to float for latitude and longitude
                lat = float(element.lat) if isinstance(element.lat, Decimal) else element.lat
                lon = float(element.lon) if isinstance(element.lon, Decimal) else element.lon
                district_info = {
                    "display_name": display_name,
                    "name": element.tags["name:en"],
                    "place_id": element.id,
                    "latitude": lat,
                    "longitude": lon
                }
                districts.append(district_info)
                
    except Exception as e:
        print(f"An error occurred: {e}")
    
    # Save the list of dictionaries to a JSON file
    with open("districts_across_levels.json", "w") as outfile:
        json.dump(districts, outfile, indent=4)

if __name__ == "__main__":
    get_districts_across_levels_and_save_to_json("JP")
