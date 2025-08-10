
import statsapi
from datetime import datetime, timedelta

"""
params: player_name (str) - Full name of the player (e.g., 'Shohei Ohtani')
        team_id (int) - Team ID (default 119 for Dodgers)
        season (int) - Season year (default 2025)
returns: dict - Player's last 5 games statline with keys: avg, hits, rbi, games, obp, slg, so
summary: Get the last 5 completed games stats for a player including OPS components
"""
def get_player_last_5_games(player_name, team_id=119, season=2025):
    player_lookup = statsapi.lookup_player(player_name)
    if not player_lookup:
        print(f"Could not find player: {player_name}")
        return None
    
    player_id = f"ID{player_lookup[0]['id']}"
    print(f"Found {player_name} - ID: {player_id}")
    
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    team_schedule = statsapi.schedule(
        team = team_id,
        season = season,
        start_date = f'{season}-01-01',
        end_date = yesterday
    )
    
    last_5_games = []
    
    for game in reversed(team_schedule):
        game_id = game['game_id']
        
        try:
            boxscore = statsapi.boxscore_data(game_id)
            
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
                
                if at_bats > 0:
                    game_info = {
                        "date": game['game_date'],
                        "opponent": game['away_name'] if side == 'home' else game['home_name'],
                        "at_bats": at_bats,
                        "hits": batting_stats.get('hits', 0),
                        "rbi": batting_stats.get('rbi', 0),
                        "hr": batting_stats.get('homeRuns', 0),
                        "walks": batting_stats.get('baseOnBalls', 0),
                        "hit_by_pitch": batting_stats.get('hitByPitch', 0),
                        "sacrifice_flys": batting_stats.get('sacrificeFlies', 0),
                        "total_bases": batting_stats.get('totalBases', 0),
                        "strikeouts": batting_stats.get('strikeOuts', 0)
                    }
                    
                    last_5_games.append(game_info)
                    
                    if len(last_5_games) == 5:
                        break
                    
        except Exception as e:
            print(f"Error processing game {game_id}: {e}")
    
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
        "games": len(last_5_games)
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
returns: dict - Pitcher's last 3 games statline with keys: era, whip, k, ip, games
summary: Get the last 3 completed games stats for a pitcher
"""
def get_pitcher_last_3_games(player_name, team_id=119, season=2025):
    player_lookup = statsapi.lookup_player(player_name)
    if not player_lookup:
        print(f"Could not find pitcher: {player_name}")
        return None
    
    player_id = f"ID{player_lookup[0]['id']}"
    print(f"Found pitcher {player_name} - ID: {player_id}")
    
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    team_schedule = statsapi.schedule(
        team = team_id,
        season = season,
        start_date = f'{season}-01-01',
        end_date = yesterday
    )
    
    last_3_games = []
    
    for game in reversed(team_schedule):
        game_id = game['game_id']
        
        try:
            boxscore = statsapi.boxscore_data(game_id)
            
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



        
        








