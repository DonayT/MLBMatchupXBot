from geopy.geocoders import Nominatim

def get_city_state(place_name):
    geolocator = Nominatim(user_agent="place_locator")
    location = geolocator.geocode(place_name)

    if location:
        address = location.raw.get('display_name', '')
        parts = address.split(', ')
        
        # Try to find city and state from address parts
        if len(parts) >= 5:
            city = parts[-5]
            state = parts[-4]
            return f"{city}, {state}"
        else:
            print("City and state not found in address")
            return None
    else:
        print("Location not found")
        return None

# Example usage
place = "Empire State Building"
result = get_city_state(place)
print(result)
