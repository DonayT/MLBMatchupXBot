
import statsapi
from datetime import datetime, timedelta

def get_player_last_5_games(player_name, team_id=119, season=2025):
    """
    Get the last 5 completed games stats for a player
    
    Args:
        player_name (str): Full name of the player (e.g., 'Shohei Ohtani')
        team_id (int): Team ID (default 119 for Dodgers)
        season (int): Season year (default 2025)
    
    Returns:
        dict: Player's last 5 games statline with keys: avg, hits, rbi, games
    """
    # Get player info
    player_lookup = statsapi.lookup_player(player_name)
    if not player_lookup:
        print(f"Could not find player: {player_name}")
        return None
    
    player_id = f"ID{player_lookup[0]['id']}"
    print(f"Found {player_name} - ID: {player_id}")
    
    # Get yesterday's date to exclude today's games
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    # Get team schedule (excluding today)
    team_schedule = statsapi.schedule(
        team = team_id,
        season = season,
        start_date = f'{season}-01-01',
        end_date = yesterday
    )
    
    last_5_games = []
    
    for game in reversed(team_schedule):  # Start from most recent
        game_id = game['game_id']
        
        try:
            boxscore = statsapi.boxscore_data(game_id)
            
            # Check both home and away players
            home_players = boxscore['home']['players']
            away_players = boxscore['away']['players']
            
            # Look for player
            player_found = None
            for side, players in [('home', home_players), ('away', away_players)]:
                if player_id in players:
                    player_found = (side, players[player_id])
                    break
            
            if player_found:
                side, player_data = player_found
                
                # Get batting stats
                batting_stats = player_data.get('stats', {}).get('batting', {})
                at_bats = batting_stats.get('atBats', 0)
                
                # Only include games where the player actually had at-bats
                if at_bats > 0:
                    game_info = {
                        "date": game['game_date'],
                        "opponent": game['away_name'] if side == 'home' else game['home_name'],
                        "at_bats": at_bats,
                        "hits": batting_stats.get('hits', 0),
                        "rbi": batting_stats.get('rbi', 0),
                        "hr": batting_stats.get('homeRuns', 0)
                    }
                    
                    last_5_games.append(game_info)
                    
                    # Stop after finding 5 games with at-bats
                    if len(last_5_games) == 5:
                        break
                    
        except Exception as e:
            print(f"Error processing game {game_id}: {e}")
    
    # Calculate totals
    total_hits = sum(g['hits'] for g in last_5_games)
    total_at_bats = sum(g['at_bats'] for g in last_5_games)
    total_rbi = sum(g['rbi'] for g in last_5_games)
    
    # Calculate batting average
    avg = total_hits / total_at_bats if total_at_bats > 0 else 0
    
    return {
        "player_name": player_name,
        "avg": round(avg, 3),
        "hits": total_hits,
        "rbi": total_rbi,
        "games": len(last_5_games)
    }

def get_lineup_last_5_games(lineup_data, team_id=119):
    """
    Get last 5 games stats for all players in a lineup
    
    Args:
        lineup_data (list): List of player dictionaries from lineup
        team_id (int): Team ID
    
    Returns:
        dict: Dictionary with player names as keys and their statlines as values
    """
    player_stats = {}
    
    for player in lineup_data:
        player_name = player.get('name', 'Unknown')
        if player_name != 'Unknown':
            stats = get_player_last_5_games(player_name, team_id)
            if stats:
                player_stats[player_name] = stats
    
    return player_stats

def get_pitcher_last_3_games(player_name, team_id=119, season=2025):
    """
    Get the last 3 completed games stats for a pitcher
    
    Args:
        player_name (str): Full name of the pitcher (e.g., 'Logan Gilbert')
        team_id (int): Team ID (default 119 for Dodgers)
        season (int): Season year (default 2025)
    
    Returns:
        dict: Pitcher's last 3 games statline with keys: era, whip, k, ip, games
    """
    # Get player info
    player_lookup = statsapi.lookup_player(player_name)
    if not player_lookup:
        print(f"Could not find pitcher: {player_name}")
        return None
    
    player_id = f"ID{player_lookup[0]['id']}"
    print(f"Found pitcher {player_name} - ID: {player_id}")
    
    # Get yesterday's date to exclude today's games
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    # Get team schedule (excluding today)
    team_schedule = statsapi.schedule(
        team = team_id,
        season = season,
        start_date = f'{season}-01-01',
        end_date = yesterday
    )
    
    last_3_games = []
    
    for game in reversed(team_schedule):  # Start from most recent
        game_id = game['game_id']
        
        try:
            boxscore = statsapi.boxscore_data(game_id)
            
            # Check both home and away players
            home_players = boxscore['home']['players']
            away_players = boxscore['away']['players']
            
            # Look for pitcher
            pitcher_found = None
            for side, players in [('home', home_players), ('away', away_players)]:
                if player_id in players:
                    pitcher_found = (side, players[player_id])
                    break
            
            if pitcher_found:
                side, player_data = pitcher_found
                
                # Get pitching stats
                pitching_stats = player_data.get('stats', {}).get('pitching', {})
                innings_pitched = pitching_stats.get('inningsPitched', 0)
                
                # Convert to float if it's a string, handle cases like "6.1" or "6"
                try:
                    innings_pitched = float(innings_pitched) if innings_pitched else 0
                except (ValueError, TypeError):
                    innings_pitched = 0
                
                # Only include games where the pitcher actually pitched
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
                    
                    # Stop after finding 3 games with innings pitched
                    if len(last_3_games) == 3:
                        break
                    
        except Exception as e:
            print(f"Error processing game {game_id}: {e}")
    
    # Calculate totals
    total_innings = sum(g['innings_pitched'] for g in last_3_games)
    total_earned_runs = sum(g['earned_runs'] for g in last_3_games)
    total_hits = sum(g['hits'] for g in last_3_games)
    total_walks = sum(g['walks'] for g in last_3_games)
    total_strikeouts = sum(g['strikeouts'] for g in last_3_games)
    total_wins = sum(g['wins'] for g in last_3_games)
    total_losses = sum(g['losses'] for g in last_3_games)
    
    # Calculate ERA and WHIP
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



        
        








