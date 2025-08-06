"""
Debug script for team record function
"""

import sys
import os

# Add the src directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from get_stats import get_team_record, PYBASEBALL_AVAILABLE

def debug_team_records():
    """Debug the team record function"""
    print("Debugging Team Record Function")
    print("=" * 40)
    
    print(f"1. pybaseball available: {PYBASEBALL_AVAILABLE}")
    
    # Test the function with a simple team name
    test_team = "New York Yankees"
    print(f"\n2. Testing with team: {test_team}")
    
    try:
        record = get_team_record(test_team)
        print(f"   Result: {record}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test with fallback
    print(f"\n3. Testing fallback behavior...")
    record_fallback = get_team_record("Unknown Team")
    print(f"   Fallback result: {record_fallback}")
    
    print("\n" + "=" * 40)
    print("Debug Complete!")

if __name__ == "__main__":
    debug_team_records()
