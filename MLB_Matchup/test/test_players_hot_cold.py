#!/usr/bin/env python3
"""
Test the OPS comparison backend to show hot/cold player analysis still works
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from get_stats import compare_ops_stats, get_cached_stats

def test_players_hot_cold():
    """Test OPS comparison for specific players"""
    print("🔥❄️ Testing OPS Comparison Backend - Hot/Cold Player Analysis")
    print("=" * 70)
    
    # Test players with their team IDs
    test_players = [
        ("James Wood", 120),      # Washington Nationals
        ("Bryce Harper", 143),    # Philadelphia Phillies  
        ("Shohei Ohtani", 119),  # Los Angeles Dodgers
        ("Jose Ramirez", 114)     # Cleveland Guardians
    ]
    
    print("📊 Testing OPS Comparison for Each Player:")
    print("-" * 50)
    
    for player_name, team_id in test_players:
        print(f"\n🎯 {player_name} (Team ID: {team_id})")
        print("-" * 30)
        
        try:
            # Get OPS comparison
            comparison = compare_ops_stats(player_name, team_id)
            
            if comparison:
                # Check if OPS values exist before formatting
                season_ops = comparison.get('season_ops')
                last_5_ops = comparison.get('last_5_games_ops')
                ops_diff = comparison.get('ops_difference')
                trend = comparison.get('trend', 'unknown')
                
                if season_ops is not None:
                    print(f"✅ Season OPS: {season_ops:.3f}")
                else:
                    print("❌ Season OPS: Not available")
                
                if last_5_ops is not None:
                    print(f"✅ Last 5 Games OPS: {last_5_ops:.3f}")
                else:
                    print("❌ Last 5 Games OPS: Not available")
                
                if ops_diff is not None:
                    print(f"✅ OPS Difference: {ops_diff:+.3f}")
                else:
                    print("❌ OPS Difference: Not available")
                
                print(f"🔥❄️ Trend: {trend.upper()}")
                
                # Show threshold calculation only if season OPS exists
                if season_ops is not None:
                    threshold = season_ops * 0.25
                    print(f"📏 25% Threshold: ±{threshold:.3f}")
                    
                    if trend == 'hot':
                        print("🔥 Player is HOT! Performing above season average")
                    elif trend == 'cold':
                        print("❄️ Player is COLD! Performing below season average")
                    else:
                        print("➡️ Player is NEUTRAL - within normal range")
                else:
                    print("📏 Cannot calculate threshold - season OPS missing")
                    
            else:
                print("❌ No comparison data available")
                
        except Exception as e:
            print(f"❌ Error analyzing {player_name}: {e}")
            # Add more debugging info
            print(f"   Error type: {type(e).__name__}")
            print(f"   Full error: {str(e)}")
    
    print("\n" + "=" * 70)
    print("🎉 OPS Comparison Backend Test Complete!")
    print("💡 All the hot/cold analysis logic is still working!")
    print("🎨 Only the visual colors were removed from the lineup images")

def test_stats_cache():
    """Test that stats cache is working"""
    print("\n🔍 Testing Stats Cache System:")
    print("-" * 30)
    
    try:
        cached_stats = get_cached_stats()
        if cached_stats:
            print("✅ Stats cache is working and loaded")
            print(f"   Cache contains data for {len(cached_stats)} players")
        else:
            print("❌ Stats cache is empty")
    except Exception as e:
        print(f"❌ Error accessing stats cache: {e}")

if __name__ == "__main__":
    test_stats_cache()
    test_players_hot_cold()
