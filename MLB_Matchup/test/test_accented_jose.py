#!/usr/bin/env python3
"""
Test if using accented name "José Ramírez" finds the correct player
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from players_previous_games import get_player_last_5_games
from get_stats import get_player_stats, compare_ops_stats

def test_accented_jose():
    """Test José Ramírez with accents"""
    print("🔍 Testing José Ramírez (with accents)")
    print("=" * 50)
    
    # Test both versions
    names_to_test = [
        ("Jose Ramirez", "No accents"),
        ("José Ramírez", "With accents")
    ]
    
    team_id = 114  # Cleveland Guardians
    
    for name, description in names_to_test:
        print(f"\n🎯 Testing: '{name}' ({description})")
        print("-" * 40)
        
        try:
            # Test 1: Get season stats
            print("📊 Season Stats:")
            season_stats = get_player_stats(name, team_id)
            if season_stats:
                print(f"   ✅ Found: {season_stats}")
                
                # Check if it's batting or pitching stats
                if 'ERA' in season_stats:
                    print("   ❌ PITCHING stats (wrong player)")
                elif 'AVG' in season_stats or 'OPS' in season_stats:
                    print("   ✅ BATTING stats (correct player!)")
                else:
                    print("   ❓ Unknown stats type")
            else:
                print("   ❌ No season stats found")
            
            # Test 2: Get last 5 games
            print("\n🎮 Last 5 Games:")
            last_5_games = get_player_last_5_games(name, team_id)
            if last_5_games and len(last_5_games) > 0:
                print(f"   ✅ Found {len(last_5_games)} games")
                
                # Check first game to see player type
                first_game = last_5_games[0]
                if 'at_bats' in first_game and first_game['at_bats'] > 0:
                    print("   ✅ BATTER stats (at-bats present)")
                else:
                    print("   ❌ No at-bats (might be pitcher)")
                    
            else:
                print("   ❌ No last 5 games data")
            
            # Test 3: Try OPS comparison
            print("\n🔥❄️ OPS Comparison:")
            comparison = compare_ops_stats(name, team_id)
            if comparison:
                season_ops = comparison.get('season_ops')
                last_5_ops = comparison.get('last_5_games_ops')
                trend = comparison.get('trend')
                
                if season_ops:
                    print(f"   ✅ Season OPS: {season_ops:.3f}")
                else:
                    print("   ❌ Season OPS: Not available")
                    
                if last_5_ops:
                    print(f"   ✅ Last 5 Games OPS: {last_5_ops:.3f}")
                else:
                    print("   ❌ Last 5 Games OPS: Not available")
                    
                print(f"   🔥❄️ Trend: {trend}")
            else:
                print("   ❌ OPS comparison failed")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()  # Empty line between tests

if __name__ == "__main__":
    test_accented_jose()
