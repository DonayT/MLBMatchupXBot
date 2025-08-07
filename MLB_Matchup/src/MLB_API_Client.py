import statsapi
from datetime import datetime
from zoneinfo import ZoneInfo
import get_address
from lineup_validator import LineupValidator
import re

class MLBAPIClient: 
    def __init__ (self):
        self.geolocator = None
        self.lineup_validator = LineupValidator()

    def get_schedule(self, date=None):
        if date is None: 
            date = datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d")
        return statsapi.schedule(start_date = date, end_date = date)

    def get_boxscore(self, game_id):
        return statsapi.boxscore_data(game_id)

    def get_venue_data(self, venue_id):
        if not venue_id:
            return None

        try:
            venue_data = statsapi.get('venue', {'venueIds': venue_id})
            return venue_data['venues'][0] if venue_data and venue_data.get('venues') else None
        except Exception as e:
            print(f"Error fetching venue data for venue_id {venue_id}: {e}")
            return None

    def get_team_records(self):
        """Get current team records as a dictionary"""
        try:
            standings = statsapi.standings()
            team_records = {}
            
            # Parse the standings string to extract team names and W-L records
            lines = standings.split('\n')
            
            for line in lines:
                # Look for lines that contain team names and W-L records
                match = re.search(r'\s+\d+\s+([A-Za-z\s\.]+)\s+(\d+)\s+(\d+)', line)
                if match:
                    team_name = match.group(1).strip()
                    wins = int(match.group(2))
                    losses = int(match.group(3))
                    
                    # Skip empty team names (parsing errors)
                    if team_name and len(team_name) > 2:
                        team_records[team_name] = {
                            'wins': wins,
                            'losses': losses,
                            'record': f"{wins}-{losses}"
                        }
            
            return team_records
            
        except Exception as e:
            print(f"Error getting team records: {e}")
            return {}

    def get_team_record(self, team_name):
        """Get record for a specific team"""
        team_records = self.get_team_records()
        return team_records.get(team_name, {'wins': 0, 'losses': 0, 'record': '0-0'})

    def format_game_datetime(self, game_datetime, game_date):
        if game_datetime:
            try:
                dt = datetime.fromisoformat(game_datetime.replace('Z', '+00:00'))
                dt_et = dt.astimezone(ZoneInfo("America/New_York"))
                
                formatted_date = dt_et.strftime('%m/%d/%Y')
                formatted_time = dt_et.strftime('%I:%M %p ET')
                return formatted_date, formatted_time
            except Exception as e:
                print(f"Error formatting datetime {game_datetime}: {e}")
        
        return game_date if game_date else 'TBD', 'TBD'
    
    def get_venue_location(self, venue_name):
        if venue_name == 'Unknown Venue':
            return 'Unknown City', 'Unknown State'
        
        try:
            city_state = get_address.get_city_state(venue_name)
            if city_state:
                city, state = city_state.split(', ')
                return city, state
            else:
                return 'Unknown City', 'Unknown State'
        except Exception as e:
            print(f"Error getting city/state for {venue_name}: {e}")
            return 'Unknown City', 'Unknown State'
    
    def extract_lineup_data(self, boxscore, side):
        batting_order = boxscore[side].get('battingOrder', [])
        players = boxscore[side].get('players', {})
        
        lineup = []
        if batting_order:
            for idx, pid in enumerate(batting_order, 1):
                player = players.get(f"ID{pid}", {})
                name = player.get('person', {}).get('fullName', 'Unknown')
                position = player.get('position', {}).get('abbreviation', '')
                
                # Get player stats with better error handling
                try:
                    recent_stats = self.get_player_15_games_string(name)
                    if isinstance(recent_stats, str) and not recent_stats.startswith('Error') and not recent_stats.startswith('No recent'):
                        # Extract just the stats part (after the colon)
                        stats_part = recent_stats.split(':\n')[-1] if ':\n' in recent_stats else recent_stats
                        # Make it more compact for display
                        stats_display = stats_part.replace('AVG: ', '').replace(' | HR: ', ' HR ').replace(' | RBI: ', ' RBI ').replace(' | BB: ', ' BB ').replace(' | SO: ', ' SO ')
                    else:
                        stats_display = "No recent data"
                        print(f"⚠️ No stats for {name}")
                except Exception as e:
                    print(f"❌ Error getting stats for {name}: {e}")
                    stats_display = "No recent data"
                
                lineup.append({
                    'order': idx,
                    'name': name,
                    'position': position,
                    'recent_stats': stats_display
                })
        
        return lineup
    
    def are_lineups_official(self, boxscore):
        return self.lineup_validator.are_lineups_official(boxscore)
    
    def get_last_15_games(self, player_name):
        """
        Get the last 15 games for a specific player using MLB Stats API
        
        Args:
            player_name (str): Full name of the player (e.g., 'Aaron Judge')
            
        Returns:
            list: List of dictionaries containing game stats for the player
        """
        try:
            # Get player ID and team ID
            player_lookup = statsapi.lookup_player(player_name)
            if not player_lookup:
                return f"Player '{player_name}' not found."
            
            player_data = player_lookup[0]
            player_id = player_data['id']
            team_id = player_data.get('currentTeam', {}).get('id', None)

            if not team_id:
                # Try to get team from detailed player info
                player_info = statsapi.get("person", {"personId": player_id})['people'][0]
                team_id = player_info.get('currentTeam', {}).get('id', None)
                
                if not team_id:
                    return f"No team information found for {player_name}."

            # Get recent games (use a smaller date range for faster performance)
            from datetime import datetime, timedelta
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=60)).strftime('%Y-%m-%d')  # Reduced to 60 days for speed
            
            recent_schedule = statsapi.schedule(team=team_id, start_date=start_date, end_date=end_date)
            
            if not recent_schedule:
                return f"No recent games found for {player_name}'s team in the last 60 days."

            # Sort games by date to ensure we get the most recent ones
            recent_schedule.sort(key=lambda x: x.get('game_date', ''), reverse=True)
            
            player_game_stats = []

            for game in recent_schedule:  # Now going forward through sorted games
                try:
                    game_id = game.get('game_id')  # Use 'game_id' instead of 'gamePk'
                    if not game_id:
                        continue
                        
                    boxscore = statsapi.boxscore_data(game_id)

                    # Check if player played for home or away
                    for side in ['home', 'away']:
                        players = boxscore[side]['players']
                        for pid, pdata in players.items():
                            if pdata['person']['id'] == player_id:
                                # Grab stats
                                stats = pdata.get('stats', {}).get('batting', {})
                                at_bats = stats.get('atBats', 0)
                                
                                # Only include games where the player actually had at-bats (like the official website)
                                if at_bats > 0:
                                    date = game.get('game_date', 'Unknown')
                                    opponent = game.get('away_name', 'Unknown') if side == 'home' else game.get('home_name', 'Unknown')
                                    player_game_stats.append({
                                        'date': date,
                                        'opponent': opponent,
                                        'AB': at_bats,
                                        'H': stats.get('hits', 0),
                                        'HR': stats.get('homeRuns', 0),
                                        'RBI': stats.get('rbi', 0),
                                        'BB': stats.get('baseOnBalls', 0),
                                        'SO': stats.get('strikeOuts', 0)
                                    })
                                break  # Found him
                        
                except Exception as e:
                    print(f"Error processing game: {e}")
                    continue
            
            # Sort all found games by date (most recent first) and take the first 15
            player_game_stats.sort(key=lambda x: x['date'], reverse=True)
            player_game_stats = player_game_stats[:15]

            return player_game_stats
            
        except Exception as e:
            return f"Error getting game history for {player_name}: {e}"
    
    def get_player_15_games_string(self, player_name, games=15):
        """
        Get a formatted string summary of player's recent performance
        
        Args:
            player_name (str): Full name of the player
            games (int): Number of recent games to analyze (default 15)
            
        Returns:
            str: Formatted performance summary string
        """
        game_stats = self.get_last_15_games(player_name)
        
        if isinstance(game_stats, str):  # Error message
            return game_stats
        
        if not game_stats:
            return f"No recent games found for {player_name}"
        
        # Calculate totals
        total_ab = sum(game['AB'] for game in game_stats)
        total_hits = sum(game['H'] for game in game_stats)
        total_hr = sum(game['HR'] for game in game_stats)
        total_rbi = sum(game['RBI'] for game in game_stats)
        
        # Calculate batting average
        avg = total_hits / total_ab if total_ab > 0 else 0
        
        summary = f"{player_name} - Last {len(game_stats)} games:\n"
        summary += f"AVG: .{int(avg*1000):03d} | HR: {total_hr} | RBI: {total_rbi}"
        
        return summary
        
        