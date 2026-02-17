"""
Stats Manager Module
Handles all pybaseball functionality and player statistics retrieval
"""

import random
from datetime import datetime

# Add pybaseball for enhanced stats
try:
    import pybaseball
    PYBASEBALL_AVAILABLE = True
    print("pybaseball loaded successfully")
except ImportError:
    PYBASEBALL_AVAILABLE = False
    print("pybaseball not available - install with: pip install pybaseball")

# Global cache to avoid repeated API calls - MAJOR PERFORMANCE OPTIMIZATION  
_stats_cache = {}
_pitcher_data = None
_batting_data = None  
_cache_initialized = False

def initialize_stats_cache():
    """Initialize the stats cache once per session - prevents slow repeated API calls"""
    global _pitcher_data, _batting_data, _cache_initialized
    
    if _cache_initialized or not PYBASEBALL_AVAILABLE:
        return
    
    try:
        current_year = datetime.now().year
        
        # Fetch all data once instead of per-player
        _pitcher_data = pybaseball.pitching_stats(current_year, qual=0)
        _batting_data = pybaseball.batting_stats(current_year, qual=0) 
        _cache_initialized = True
        print("Stats cache initialized successfully")
    except Exception as e:
        print(f"Error initializing stats cache: {e}")

def clear_stats_cache():
    """Clear the stats cache to allow re-initialization for new days"""
    global _pitcher_data, _batting_data, _cache_initialized
    _pitcher_data = None
    _batting_data = None
    _cache_initialized = False
    print("Stats cache cleared for new day")

def get_player_stats(player_name, is_pitcher=False, position=''):
    """Get player stats using pybaseball with guaranteed fallback"""
    if not PYBASEBALL_AVAILABLE:
        return get_fallback_stats(is_pitcher, position)
    
    try:
        current_year = datetime.now().year
        
        if is_pitcher or position in ['P', 'SP', 'RP', 'CP']:
            # Get pitcher stats with lower qualification threshold
            pitcher_stats = pybaseball.pitching_stats(current_year, qual=0)  # All pitchers
            # Try multiple matching strategies
            pitcher_row = None
            
            # Try exact name match first
            exact_match = pitcher_stats[pitcher_stats['Name'].str.lower() == player_name.lower()]
            if not exact_match.empty:
                pitcher_row = exact_match.iloc[0]
            else:
                # Try last name match
                last_name = player_name.split()[-1]
                lastname_match = pitcher_stats[pitcher_stats['Name'].str.contains(last_name, case=False, na=False)]
                if not lastname_match.empty:
                    pitcher_row = lastname_match.iloc[0]
            
            if pitcher_row is not None:
                era = pitcher_row['ERA']
                wins = pitcher_row['W']
                losses = pitcher_row['L']
                return f"{int(wins)}-{int(losses)} {era:.2f} ERA"
        else:
            # Get batter stats with lower qualification threshold
            batting_stats = pybaseball.batting_stats(current_year, qual=0)  # All batters
            batter_row = None
            
            # Try exact name match first
            exact_match = batting_stats[batting_stats['Name'].str.lower() == player_name.lower()]
            if not exact_match.empty:
                batter_row = exact_match.iloc[0]
            else:
                # Try last name match
                last_name = player_name.split()[-1]
                lastname_match = batting_stats[batting_stats['Name'].str.contains(last_name, case=False, na=False)]
                if not lastname_match.empty:
                    batter_row = lastname_match.iloc[0]
            
            if batter_row is not None:
                avg = batter_row['AVG']
                hr = batter_row['HR']
                rbi = batter_row['RBI']
                ops = batter_row['OPS']
                return f".{int(avg*1000):03d} {int(hr)} HR {int(rbi)} RBI {ops:.3f} OPS"
                
    except Exception as e:
        print(f"Error fetching stats for {player_name}: {e}")
    
    # Always return fallback stats if nothing found
    return get_fallback_stats(is_pitcher or position in ['P', 'SP', 'RP', 'CP'], position)

def get_fallback_stats(is_pitcher, position=''):
    """Generate realistic fallback stats when real data isn't available"""
    if is_pitcher or position in ['P', 'SP', 'RP', 'CP']:
        # Generate realistic pitcher stats (no commas)
        # wins = random.randint(0, 12)
        # losses = random.randint(0, 8)
        # era = round(random.uniform(2.50, 5.50), 2)
        wins = 0
        losses = 0
        era = 0.00
        return f"{wins}-{losses} {era:.2f} ERA"
    else:
        # Generate realistic batter stats (no commas)
        # avg = random.randint(220, 320)
        # hr = random.randint(5, 35)
        # rbi = random.randint(25, 95)
        avg = .000
        hr = 0
        rbi = 0
        return f".{avg:03d} {hr} HR {rbi} RBI"

def get_cached_stats():
    """Get cached stats data for debugging/testing"""
    return {
        'pitcher_data': _pitcher_data,
        'batting_data': _batting_data,
        'cache_initialized': _cache_initialized,
        'pybaseball_available': PYBASEBALL_AVAILABLE
    }

def compare_ops_stats(player_name, team_id=119, team_schedule=None):
    """
    Compare season OPS (from pybaseball) vs last 5 games OPS (from statsapi)

    params: player_name (str) - Player name to compare
            team_id (int) - Team ID for statsapi lookup
            team_schedule (list, optional) - Pre-fetched team schedule to avoid redundant API calls
    returns: dict - Comparison data with both OPS values and difference
    """
    try:
        # Get season OPS from pybaseball cache
        season_stats = get_player_stats(player_name, is_pitcher=False)
        season_ops = None

        # Extract OPS from the stats string (format: ".315 25 HR 89 RBI 0.847 OPS")
        if season_stats and "OPS" in season_stats:
            try:
                # Find the OPS value before "OPS" in the string
                ops_part = season_stats.split("OPS")[0].strip()
                season_ops = float(ops_part.split()[-1])
            except (ValueError, IndexError):
                season_ops = None

        # Get last 5 games OPS from statsapi - pass pre-fetched schedule
        try:
            from players_previous_games import get_player_last_5_games
            last_5_stats = get_player_last_5_games(player_name, team_id, team_schedule=team_schedule)
            
            # NEW LOGIC: Check if player has sufficient recent activity
            if last_5_stats and last_5_stats.get('recent_activity') == 'insufficient':
                games_with_pa = last_5_stats.get('games_with_pa_in_last_10', 0)
                print(f"⚠️ {player_name}: Only {games_with_pa}/10 recent games with PAs - marking as neutral but showing stats")
                # Return the OPS for display purposes, but mark trend as neutral
                last_5_ops = last_5_stats['ops']
                return {
                    "player_name": player_name,
                    "season_ops": season_ops,
                    "last_5_games_ops": last_5_ops,
                    "ops_difference": None,  # Can't calculate difference due to insufficient data
                    "trend": "neutral",
                    "reason": "insufficient_recent_activity",
                    "games_with_pa_in_last_10": games_with_pa
                }
            
            last_5_ops = last_5_stats['ops'] if last_5_stats else None
        except Exception as e:
            print(f"Error getting last 5 games stats: {e}")
            last_5_ops = None
        
        # Calculate difference if both values exist
        ops_difference = None
        if season_ops is not None and last_5_ops is not None:
            ops_difference = last_5_ops - season_ops
        
        return {
            "player_name": player_name,
            "season_ops": season_ops,
            "last_5_games_ops": last_5_ops,
            "ops_difference": ops_difference,
            "trend": "hot" if ops_difference and ops_difference > (season_ops * 0.25) else 
                     "cold" if ops_difference and ops_difference < -(season_ops * 0.25) else "neutral"
        }
        
    except Exception as e:
        print(f"Error comparing OPS stats for {player_name}: {e}")
        return None 

def compare_lineup_ops_stats(lineup_data, team_id=119):
    """
    Compare season OPS vs last 5 games OPS for all players in a lineup
    
    params: lineup_data (list) - List of player dictionaries from lineup
            team_id (int) - Team ID for statsapi lookup
    returns: dict - Dictionary with player names as keys and their OPS comparisons
    """
    lineup_comparison = {}
    
    for player in lineup_data:
        player_name = player.get('name', 'Unknown')
        if player_name != 'Unknown':
            # Skip pitchers (they don't have batting OPS)
            position = player.get('position', '')
            if position in ['P', 'SP', 'RP', 'CP']:
                continue
                
            comparison = compare_ops_stats(player_name, team_id)
            if comparison:
                lineup_comparison[player_name] = comparison
    
    return lineup_comparison

def get_lineup_ops_summary(lineup_data, team_id=119):
    """
    Get a summary of OPS trends for an entire lineup
    
    params: lineup_data (list) - List of player dictionaries from lineup
            team_id (int) - Team ID for statsapi lookup
    returns: dict - Summary statistics for the lineup
    """
    lineup_comparison = compare_lineup_ops_stats(lineup_data, team_id)
    
    if not lineup_comparison:
        return None
    
    hot_players = []
    cold_players = []
    neutral_players = []
    
    total_season_ops = 0
    total_recent_ops = 0
    valid_comparisons = 0
    
    for player_name, comparison in lineup_comparison.items():
        if comparison['trend'] == 'hot':
            hot_players.append(player_name)
            print(f"🔥 {player_name}: HOT trend")
        elif comparison['trend'] == 'cold':
            cold_players.append(player_name)
            print(f"❄️ {player_name}: COLD trend")
        else:
            neutral_players.append(player_name)
            reason = comparison.get('reason', 'no_trend')
            if reason == 'insufficient_recent_activity':
                games_with_pa = comparison.get('games_with_pa_in_last_10', 0)
                print(f"⚪ {player_name}: NEUTRAL (only {games_with_pa}/10 recent games with PAs)")
            else:
                print(f"⚪ {player_name}: NEUTRAL (no significant trend)")
        
        # Sum up OPS values for averages
        if comparison['season_ops'] is not None and comparison['last_5_games_ops'] is not None:
            total_season_ops += comparison['season_ops']
            total_recent_ops += comparison['last_5_games_ops']
            valid_comparisons += 1
    
    avg_season_ops = total_season_ops / valid_comparisons if valid_comparisons > 0 else 0
    avg_recent_ops = total_recent_ops / valid_comparisons if valid_comparisons > 0 else 0
    
    return {
        "total_players": len(lineup_comparison),
        "hot_players": hot_players,
        "cold_players": cold_players,
        "neutral_players": neutral_players,
        "hot_count": len(hot_players),
        "cold_count": len(cold_players),
        "neutral_count": len(neutral_players),
        "avg_season_ops": round(avg_season_ops, 3),
        "avg_recent_ops": round(avg_recent_ops, 3),
        "lineup_trend": "hot" if len(hot_players) > len(cold_players) else 
                        "cold" if len(cold_players) > len(hot_players) else "neutral",
        "player_comparisons": lineup_comparison
    } 