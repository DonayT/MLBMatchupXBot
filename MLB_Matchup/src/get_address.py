import json
import os
from geopy.geocoders import Nominatim

def load_state_abbreviations():
    """Load state abbreviations from JSON file"""
    try:
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'stateAbbreviations.json')
        with open(config_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading state abbreviations: {e}")
        return {}

def convert_state_to_abbreviation(state_name):
    """Convert state name to abbreviation using JSON mapping"""
    state_abbreviations = load_state_abbreviations()
    
    # Try exact match first
    if state_name in state_abbreviations:
        return state_abbreviations[state_name]
    
    # Try case-insensitive match
    for full_name, abbreviation in state_abbreviations.items():
        if state_name.lower() == full_name.lower():
            return abbreviation
    
    # If no match found, return original state name
    return state_name

def get_city_state(place_name):
    geolocator = Nominatim(user_agent="place_locator")
    location = geolocator.geocode(place_name)

    if location:
        address = location.raw.get('display_name', '')
        print(address)
        parts = address.split(', ')
        
        # Try to find city and state from address parts
        # Look for patterns in the address parts
        city = None
        state = None
        
        # Common patterns for US addresses
        state_abbreviations = load_state_abbreviations()
        for i, part in enumerate(parts):
            # Look for state (usually near the end, before zip code)
            if part in state_abbreviations:
                state = part
                # City is usually 1-2 parts before state, but not if it's "County"
                if i >= 1:
                    potential_city = parts[i-1]
                    if "County" not in potential_city:
                        city = potential_city
                    elif i >= 2:
                        # If the previous part was a county, look one more back
                        city = parts[i-2]
                break
        
        # If we found both city and state
        if city and state:
            # Convert state name to abbreviation
            state_abbr = convert_state_to_abbreviation(state)
            return f"{city}, {state_abbr}"
        else:
            print("City and state not found in address")
            return None
    else:
        print("Location not found")
        return None



# Example usage
if __name__ == "__main__":
    # Test state abbreviation function
    print("Testing state abbreviation function:")
    test_states = ["New York", "California", "Texas", "Florida", "Unknown State"]
    for state in test_states:
        abbr = convert_state_to_abbreviation(state)
        print(f"  {state} -> {abbr}")
    
    print("\nTesting city/state function:")
    places = ["Empire State Building", "PNC Park", "Polk Theatre"]
    for place in places:
        result = get_city_state(place)
        print(f"  {place} -> {result}")
