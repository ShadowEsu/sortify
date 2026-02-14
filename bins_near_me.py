import googlemaps
import json
from dotenv import load_dotenv 

# CONFIGURATION
load_dotenv()
API_KEY = 'GOOGLE_MAPS_API_KEY'

def get_coordinates(gmaps, address):
    """Converts a text address into generic latitude/longitude."""
    try:
        geocode_result = gmaps.geocode(address)
        if geocode_result:
            location = geocode_result[0]['geometry']['location']
            return location
        else:
            print(f"Error: Could not find coordinates for address: {address}")
            return None
    except Exception as e:
        print(f"Geocoding error: {e}")
        return None

def find_nearest_facilities(gmaps, location, keywords, radius_meters=5000):
    """
    Searches for places nearby based on keywords.
    Returns a dictionary of results.
    """
    results = {}
    
    for category, keyword in keywords.items():
        print(f"Searching for {category} ({keyword})...")
        try:
            # places_nearby searches based on location and radius
            response = gmaps.places_nearby(
                location=location,
                keyword=keyword,
                radius=radius_meters,
                rank_by='prominence' # Or use rank_by='distance' (requires name/keyword/type)
            )
            
            places = []
            for place in response.get('results', [])[:3]: # Limit to top 3 results per category
                places.append({
                    'name': place.get('name'),
                    'address': place.get('vicinity'),
                    'rating': place.get('rating', 'N/A'),
                    'location': place.get('geometry', {}).get('location')
                })
            
            results[category] = places
            
        except Exception as e:
            print(f"Error searching for {keyword}: {e}")
            results[category] = []
            
    return results

def main():
    # 1. Initialize the client
    try:
        gmaps = googlemaps.Client(key=API_KEY)
    except ValueError:
        print("Please provide a valid API Key in the script.")
        return

    # 2. Define your search center (You can change this to your current location)
    user_address = "San Francisco, CA" 
    print(f"Target Location: {user_address}")
    
    # 3. Get coordinates
    location = get_coordinates(gmaps, user_address)
    
    if location:
        # 4. Define search terms
        # Google Maps works best with facility-type keywords
        search_terms = {
            'Recycle': 'recycling center',
            'Trash/Dump': 'waste disposal service', 
            'Compost': 'composting service' 
        }

        # 5. Execute Search
        bins_nearby = find_nearest_facilities(gmaps, location, search_terms)

        # 6. Print Results
        print("\n--- RESULTS ---")
        for category, places in bins_nearby.items():
            print(f"\n[{category.upper()}]")
            if not places:
                print("  No facilities found nearby.")
            for place in places:
                print(f"  - {place['name']}")
                print(f"    Addr: {place['address']}")
                print(f"    Rating: {place['rating']}")

if __name__ == "__main__":
    main()