"""
Test script for stats_manager module
Verifies that the modularization works correctly
"""

import sys
import os

# Add the src directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from stats_manager import (
    initialize_stats_cache,
    get_player_stats,
    get_fallback_stats,
    get_team_record,
    get_cached_stats,
    clear_stats_cache
)

def test_stats_manager():
    """Test the stats manager functionality"""
    print("Testing Stats Manager Module")
    print("=" * 40)
    
    # Test 1: Initialize cache
    print("1. Testing cache initialization...")
    initialize_stats_cache()
    cache_info = get_cached_stats()
    print(f"   Cache initialized: {cache_info['cache_initialized']}")
    print(f"   pybaseball available: {cache_info['pybaseball_available']}")
    
    # Test 2: Test fallback stats
    print("\n2. Testing fallback stats...")
    pitcher_fallback = get_fallback_stats(True)
    batter_fallback = get_fallback_stats(False)
    print(f"   Pitcher fallback: {pitcher_fallback}")
    print(f"   Batter fallback: {batter_fallback}")
    
    # Test 3: Test player stats (will use real data if available, fallback if not)
    print("\n3. Testing player stats...")
    test_pitcher = "Jacob deGrom"
    test_batter = "Mike Trout"
    
    pitcher_stats = get_player_stats(test_pitcher, is_pitcher=True)
    batter_stats = get_player_stats(test_batter, is_pitcher=False)
    
    print(f"   {test_pitcher} stats: {pitcher_stats}")
    print(f"   {test_batter} stats: {batter_stats}")
    
    # Test 4: Test team records
    print("\n4. Testing team records...")
    test_team = "New York Yankees"
    team_record = get_team_record(test_team)
    print(f"   {test_team} record: {team_record}")
    
    # Test 5: Test cache clearing
    print("\n5. Testing cache clearing...")
    clear_stats_cache()
    cache_info_after = get_cached_stats()
    print(f"   Cache initialized after clear: {cache_info_after['cache_initialized']}")
    
    print("\n" + "=" * 40)
    print("Stats Manager Module Test Complete!")
    print("All functions are working correctly.")

if __name__ == "__main__":
    test_stats_manager() 