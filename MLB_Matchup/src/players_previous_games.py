
import statsapi
from datetime import datetime, timedelta
import sys
import os

# Add utils directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'utils'))

from api_cache import get_cache

"""
params: player_name (str) - Full name of the player (e.g., 'Shohei Ohtani')
        team_id (int) - Team ID (default 119 for Dodgers)
        season (int) - Season year (default 2025)
        team_schedule (list, optional) - Pre-fetched team schedule to avoid redundant API calls
returns: dict - Player's last 5 games statline with keys: avg, hits, rbi, games, obp, slg, so
summary: Get the last 5 completed games stats for a player including OPS components
"""
def get_player_last_5_games(player_name, team_id=119, season=2025, team_schedule=None):
    cache = get_cache()

    # Use cache for player lookup
    player_id_num = cache.get_player_id(player_name)
    if not player_id_num:
        print(f"Could not find player: {player_name}")
        return None

    player_id = f"ID{player_id_num}"
    print(f"Found {player_name} - ID: {player_id}")

    # Use pre-fetched schedule if provided, otherwise fetch it
    if team_schedule is None:
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        team_schedule = cache.get_team_schedule(
            team_id=team_id,
            season=season,
            start_date=f'{season}-01-01',
            end_date=yesterday
        )
    
    # NEW LOGIC: Look at last 10 games instead of entire season
    last_10_games = team_schedule[-10:] if len(team_schedule) >= 10 else team_schedule
    last_10_games = list(reversed(last_10_games))  # Most recent first
    
    last_5_games = []
    games_with_pa = 0  # Count games where player had a Plate Appearance
    
    # First pass: Check all 10 games to see how many the player appeared in
    for game in last_10_games:
        game_id = game['game_id']

        try:
            # Use cache for boxscore data
            boxscore = cache.get_boxscore(game_id)
            if not boxscore:
                continue
            
            home_players = boxscore['home']['players']
            away_players = boxscore['away']['players']
            
            player_found = None
            for side, players in [('home', home_players), ('away', away_players)]:
                if player_id in players:
                    player_found = (side, players[player_id])
                    break
            
            if player_found:
                side, player_data = player_found
                
                batting_stats = player_data.get('stats', {}).get('batting', {})
                at_bats = batting_stats.get('atBats', 0)
                walks = batting_stats.get('baseOnBalls', 0)
                hit_by_pitch = batting_stats.get('hitByPitch', 0)
                sacrifice_flys = batting_stats.get('sacrificeFlies', 0)
                
                # Calculate Plate Appearances (AB + BB + HBP + SF)
                plate_appearances = at_bats + walks + hit_by_pitch + sacrifice_flys
                
                if plate_appearances > 0:
                    games_with_pa += 1
                    
                    # Only collect stats for the last 5 games they appeared in
                    if len(last_5_games) < 5:
                        game_info = {
                            "date": game['game_date'],
                            "opponent": game['away_name'] if side == 'home' else game['home_name'],
                            "at_bats": at_bats,
                            "hits": batting_stats.get('hits', 0),
                            "rbi": batting_stats.get('rbi', 0),
                            "hr": batting_stats.get('homeRuns', 0),
                            "walks": walks,
                            "hit_by_pitch": hit_by_pitch,
                            "sacrifice_flys": sacrifice_flys,
                            "doubles": batting_stats.get('doubles', 0),
                            "triples": batting_stats.get('triples', 0),
                            "strikeouts": batting_stats.get('strikeOuts', 0),
                            "plate_appearances": plate_appearances
                        }
                        
                        # Calculate total bases manually since statsapi doesn't provide it
                        game_info["total_bases"] = (game_info["hits"] + 
                                                  game_info["doubles"] + 
                                                  (2 * game_info["triples"]) + 
                                                  (3 * game_info["hr"]))
                        
                        last_5_games.append(game_info)
                    
        except Exception as e:
            print(f"Error processing game {game_id}: {e}")
    
    # NEW LOGIC: Check if player has sufficient recent activity (5+ games with PAs in last 10)
    if len(last_10_games) >= 10:
        if games_with_pa < 5:
            print(f"⚠️ {player_name}: Only {games_with_pa}/10 recent games with PAs - marking as neutral")
            # Still return stats but indicate insufficient recent activity
            if not last_5_games:
                return None
            
            # Calculate stats from available games
            total_hits = total_at_bats = total_rbi = total_walks = 0
            total_hbp = total_sf = total_bases = total_strikeouts = 0
            
            for game in last_5_games:
                total_hits += game['hits']
                total_at_bats += game['at_bats']
                total_rbi += game['rbi']
                total_walks += game['walks']
                total_hbp += game['hit_by_pitch']
                total_sf += game['sacrifice_flys']
                total_bases += game['total_bases']
                total_strikeouts += game['strikeouts']
            
            avg = total_hits / total_at_bats if total_at_bats > 0 else 0
            plate_appearances = total_at_bats + total_walks + total_hbp + total_sf
            obp = (total_hits + total_walks + total_hbp) / plate_appearances if plate_appearances > 0 else 0
            slg = total_bases / total_at_bats if total_at_bats > 0 else 0
            ops = obp + slg
            
            return {
                "player_name": player_name,
                "avg": round(avg, 3),
                "ops": round(ops, 3),
                "hits": total_hits,
                "rbi": total_rbi,
                "so": total_strikeouts,
                "games": len(last_5_games),
                "recent_activity": "insufficient",  # Mark as insufficient for trend calculation
                "games_with_pa_in_last_10": games_with_pa
            }
    
    # Player meets the requirement or we don't have 10 games to check
    if not last_5_games:
        return None
    
    total_hits = total_at_bats = total_rbi = total_walks = 0
    total_hbp = total_sf = total_bases = total_strikeouts = 0
    
    for game in last_5_games:
        total_hits += game['hits']
        total_at_bats += game['at_bats']
        total_rbi += game['rbi']
        total_walks += game['walks']
        total_hbp += game['hit_by_pitch']
        total_sf += game['sacrifice_flys']
        total_bases += game['total_bases']
        total_strikeouts += game['strikeouts']
    
    avg = total_hits / total_at_bats if total_at_bats > 0 else 0
    
    plate_appearances = total_at_bats + total_walks + total_hbp + total_sf
    obp = (total_hits + total_walks + total_hbp) / plate_appearances if plate_appearances > 0 else 0
    
    slg = total_bases / total_at_bats if total_at_bats > 0 else 0
    
    ops = obp + slg
    
    return {
        "player_name": player_name,
        "avg": round(avg, 3),
        "ops": round(ops, 3),
        "hits": total_hits,
        "rbi": total_rbi,
        "so": total_strikeouts,
        "games": len(last_5_games),
        "recent_activity": "sufficient",  # Mark as sufficient for trend calculation
        "games_with_pa_in_last_10": games_with_pa
    }

"""
params: lineup_data (list) - List of player dictionaries from lineup
        team_id (int) - Team ID
returns: dict - Dictionary with player names as keys and their statlines as values
summary: Get last 5 games stats for all players in a lineup
"""
def get_lineup_last_5_games(lineup_data, team_id=119):
    player_stats = {}
    
    for player in lineup_data:
        player_name = player.get('name', 'Unknown')
        if player_name != 'Unknown':
            stats = get_player_last_5_games(player_name, team_id)
            if stats:
                player_stats[player_name] = stats
    
    return player_stats

"""
params: player_name (str) - Full name of the pitcher (e.g., 'Logan Gilbert')
        team_id (int) - Team ID (default 119 for Dodgers)
        season (int) - Season year (default 2025)
        team_schedule (list, optional) - Pre-fetched team schedule to avoid redundant API calls
returns: dict - Pitcher's last 3 games statline with keys: era, whip, k, ip, games
summary: Get the last 3 completed games stats for a pitcher
"""
def get_pitcher_last_3_games(player_name, team_id=119, season=2025, team_schedule=None):
    cache = get_cache()

    # Use cache for player lookup
    player_id_num = cache.get_player_id(player_name)
    if not player_id_num:
        print(f"Could not find pitcher: {player_name}")
        return None

    player_id = f"ID{player_id_num}"
    print(f"Found pitcher {player_name} - ID: {player_id}")

    # Use pre-fetched schedule if provided, otherwise fetch it
    if team_schedule is None:
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        team_schedule = cache.get_team_schedule(
            team_id=team_id,
            season=season,
            start_date=f'{season}-01-01',
            end_date=yesterday
        )
    
    last_3_games = []
    
    for game in reversed(team_schedule):
        game_id = game['game_id']

        try:
            # Use cache for boxscore data
            boxscore = cache.get_boxscore(game_id)
            if not boxscore:
                continue
            
            home_players = boxscore['home']['players']
            away_players = boxscore['away']['players']
            
            pitcher_found = None
            for side, players in [('home', home_players), ('away', away_players)]:
                if player_id in players:
                    pitcher_found = (side, players[player_id])
                    break
            
            if pitcher_found:
                side, player_data = pitcher_found
                
                pitching_stats = player_data.get('stats', {}).get('pitching', {})
                innings_pitched = pitching_stats.get('inningsPitched', 0)
                
                try:
                    innings_pitched = float(innings_pitched) if innings_pitched else 0
                except (ValueError, TypeError):
                    innings_pitched = 0
                
                if innings_pitched > 0:
                    game_info = {
                        "date": game['game_date'],
                        "opponent": game['away_name'] if side == 'home' else game['home_name'],
                        "innings_pitched": innings_pitched,
                        "earned_runs": pitching_stats.get('earnedRuns', 0),
                        "hits": pitching_stats.get('hits', 0),
                        "walks": pitching_stats.get('baseOnBalls', 0),
                        "strikeouts": pitching_stats.get('strikeOuts', 0),
                        "wins": pitching_stats.get('wins', 0),
                        "losses": pitching_stats.get('losses', 0)
                    }
                    
                    last_3_games.append(game_info)
                    
                    if len(last_3_games) == 3:
                        break
                    
        except Exception as e:
            print(f"Error processing game {game_id}: {e}")
    
    total_innings = sum(g['innings_pitched'] for g in last_3_games)
    total_earned_runs = sum(g['earned_runs'] for g in last_3_games)
    total_hits = sum(g['hits'] for g in last_3_games)
    total_walks = sum(g['walks'] for g in last_3_games)
    total_strikeouts = sum(g['strikeouts'] for g in last_3_games)
    total_wins = sum(g['wins'] for g in last_3_games)
    total_losses = sum(g['losses'] for g in last_3_games)
    
    era = (total_earned_runs * 9) / total_innings if total_innings > 0 else 0
    whip = (total_hits + total_walks) / total_innings if total_innings > 0 else 0
    
    return {
        "player_name": player_name,
        "era": round(era, 2),
        "whip": round(whip, 2),
        "k": total_strikeouts,
        "ip": round(total_innings, 1),
        "wins": total_wins,
        "losses": total_losses,
        "games": len(last_3_games)
    }



        
        








