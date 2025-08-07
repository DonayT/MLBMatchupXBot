"""
Test file for get_stats.py module
Tests player stats retrieval for specific players
"""

import sys
import os

# Add the src directory to the path so we can import modules
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))

from get_stats import initialize_stats_cache, get_player_stats, get_cached_stats, clear_stats_cache

def test_player_stats():
    """Test getting stats for specific players"""
    
    print("=== Testing get_stats.py ===")
    
    # Initialize the stats cache
    print("\n1. Initializing stats cache...")
    initialize_stats_cache()
    
    # Test Logan Gilbert (pitcher)
    print("\n2. Testing Logan Gilbert (pitcher)...")
    logan_gilbert_stats = get_player_stats("Logan Gilbert", is_pitcher=True)
    print(f"Logan Gilbert stats: {logan_gilbert_stats}")
    
    # Test Steven Kwan (hitter)
    print("\n3. Testing Steven Kwan (hitter)...")
    steven_kwan_stats = get_player_stats("Steven Kwan", is_pitcher=False)
    print(f"Steven Kwan stats: {steven_kwan_stats}")
    
    # Show cache status
    print("\n4. Cache status:")
    cache_info = get_cached_stats()
    print(f"Cache initialized: {cache_info['cache_initialized']}")
    print(f"Pybaseball available: {cache_info['pybaseball_available']}")
    print(f"Pitcher data loaded: {cache_info['pitcher_data'] is not None}")
    print(f"Batting data loaded: {cache_info['batting_data'] is not None}")
    
    # Test with different name formats
    print("\n5. Testing different name formats...")
    logan_gilbert_stats2 = get_player_stats("Gilbert", is_pitcher=True)
    print(f"Logan Gilbert (last name only): {logan_gilbert_stats2}")
    
    steven_kwan_stats2 = get_player_stats("Kwan", is_pitcher=False)
    print(f"Steven Kwan (last name only): {steven_kwan_stats2}")
    
    print("\n=== Test completed ===")

if __name__ == "__main__":
    test_player_stats()
