import statsapi
from datetime import datetime
from zoneinfo import ZoneInfo
import get_address
from lineup_validator import LineupValidator
from players_previous_games import get_player_last_5_games, get_pitcher_last_3_games
import re

class MLBAPIClient: 
    def __init__ (self):
        self.geolocator = None
        self.lineup_validator = LineupValidator()

    """
    params: date (str, optional) - Date in YYYY-MM-DD format, defaults to today
    returns: list - List of games scheduled for the specified date
    summary: Get MLB schedule for a specific date
    """
    def get_schedule(self, date=None):
        if date is None: 
            date = datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d")
        return statsapi.schedule(start_date = date, end_date = date)

    """
    params: game_id (int) - MLB game ID
    returns: dict - Boxscore data for the specified game
    summary: Retrieve boxscore data for a specific MLB game
    """
    def get_boxscore(self, game_id):
        return statsapi.boxscore_data(game_id)

    """
    params: venue_id (int) - MLB venue ID
    returns: dict or None - Venue information or None if not found
    summary: Get venue data for a specific MLB venue
    """
    def get_venue_data(self, venue_id):
        if not venue_id:
            return None

        try:
            venue_data = statsapi.get('venue', {'venueIds': venue_id})
            return venue_data['venues'][0] if venue_data and venue_data.get('venues') else None
        except Exception as e:
            print(f"Error fetching venue data for venue_id {venue_id}: {e}")
            return None

    """
    params: None
    returns: dict - Dictionary mapping team names to their W-L records
    summary: Get current team records from MLB standings
    """
    def get_team_records(self):
        try:
            standings = statsapi.standings()
            team_records = {}
            
            lines = standings.split('\n')
            
            for line in lines:
                match = re.search(r'\s+\d+\s+([A-Za-z\s\.]+)\s+(\d+)\s+(\d+)', line)
                if match:
                    team_name = match.group(1).strip()
                    wins = int(match.group(2))
                    losses = int(match.group(3))
                    
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

    """
    params: team_name (str) - Name of the team
    returns: dict - Team record with wins, losses, and formatted record string
    summary: Get record for a specific team
    """
    def get_team_record(self, team_name):
        team_records = self.get_team_records()
        return team_records.get(team_name, {'wins': 0, 'losses': 0, 'record': '0-0'})

    """
    params: game_datetime (str) - ISO format datetime string, game_date (str) - Fallback date
    returns: tuple - (formatted_date, formatted_time) in MM/DD/YYYY and I:M AM/PM ET format
    summary: Format game datetime to Eastern Time and readable format
    """
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
    
    """
    params: venue_name (str) - Name of the venue
    returns: tuple - (city, state) extracted from venue name
    summary: Extract city and state information from venue name
    """
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
    
    """
    params: boxscore (dict) - Game boxscore data, side (str) - 'home' or 'away'
    returns: list - List of player dictionaries with basic lineup information
    summary: Extract basic lineup data without player stats for incomplete lineups
    """
    def extract_lineup_data_basic(self, boxscore, side):
        batting_order = boxscore[side].get('battingOrder', [])
        players = boxscore[side].get('players', {})
        
        lineup = []
        if batting_order:
            for idx, pid in enumerate(batting_order, 1):
                player = players.get(f"ID{pid}", {})
                name = player.get('person', {}).get('fullName', 'Unknown')
                position = player.get('position', {}).get('abbreviation', '')
                
                lineup.append({
                    'order': idx,
                    'name': name,
                    'position': position,
                    'recent_stats': "No recent data"
                })
        
        return lineup
    
    """
    params: boxscore (dict) - Game boxscore data, side (str) - 'home' or 'away', team_id (int) - Team ID
    returns: list - List containing player lineup data with recent stats
    summary: Extract complete lineup data with recent performance statistics
    """
    def extract_lineup_data(self, boxscore, side, team_id=119):
        batting_order = boxscore[side].get('battingOrder', [])
        players = boxscore[side].get('players', {})
        
        lineup = []
        if batting_order:
            for idx, pid in enumerate(batting_order, 1):
                player = players.get(f"ID{pid}", {})
                name = player.get('person', {}).get('fullName', 'Unknown')
                position = player.get('position', {}).get('abbreviation', '')
                
                try:
                    recent_stats = get_player_last_5_games(name, team_id)
                    if recent_stats and isinstance(recent_stats, dict):
                        avg = recent_stats.get('avg', 0)
                        ops = recent_stats.get('ops', 0)
                        hits = recent_stats.get('hits', 0)
                        rbi = recent_stats.get('rbi', 0)
                        so = recent_stats.get('so', 0)
                        games = recent_stats.get('games', 0)
                        
                        if games > 0:
                            stats_display = f"AVG: {avg:.3f} / OPS: {ops:.3f} / H: {hits} / RBIs: {rbi} / SO: {so}"
                        else:
                            stats_display = "No recent data"
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
    
    """
    params: boxscore (dict) - Game boxscore data
    returns: bool - True if lineups are official, False otherwise
    summary: Check if lineups for a game are official
    """
    def are_lineups_official(self, boxscore):
        return self.lineup_validator.are_lineups_official(boxscore)
    
    """
    params: boxscore (dict) - Game boxscore data, side (str) - 'home' or 'away', team_id (int) - Team ID
    returns: list - List containing starting pitcher data with recent stats
    summary: Extract starting pitcher data with recent performance statistics
    """
    def extract_pitcher_data(self, boxscore, side, team_id=119):
        pitchers = boxscore[side].get('pitchers', [])
        players = boxscore[side].get('players', {})
        
        if not pitchers:
            return []
        
        pitcher_id = pitchers[0]
        player = players.get(f"ID{pitcher_id}", {})
        name = player.get('person', {}).get('fullName', 'Unknown')
        position = player.get('position', {}).get('abbreviation', '')
        
        try:
            recent_stats = get_pitcher_last_3_games(name, team_id)
            if recent_stats and isinstance(recent_stats, dict):
                era = recent_stats.get('era', 0)
                whip = recent_stats.get('whip', 0)
                k = recent_stats.get('k', 0)
                ip = recent_stats.get('ip', 0)
                games = recent_stats.get('games', 0)
                
                if games > 0:
                    stats_display = f"ERA: {era:.2f} WHIP: {whip:.2f} K: {k} IP: {ip}"
                else:
                    stats_display = "No recent data"
            else:
                stats_display = "No recent data"
        except Exception as e:
            print(f"❌ Error getting pitcher stats for {name}: {e}")
            stats_display = "No recent data"
        
        return [{
            'name': name,
            'position': position,
            'recent_stats': stats_display
        }]
    
    """
    params: boxscore (dict) - Game boxscore data, side (str) - 'home' or 'away'
    returns: list - List containing basic starting pitcher data without stats
    summary: Extract basic starting pitcher data for incomplete lineups
    """
    def extract_pitcher_data_basic(self, boxscore, side):
        pitchers = boxscore[side].get('pitchers', [])
        players = boxscore[side].get('players', {})
        
        if not pitchers:
            return []
        
        pitcher_id = pitchers[0]
        player = players.get(f"ID{pitcher_id}", {})
        name = player.get('person', {}).get('fullName', 'Unknown')
        position = player.get('position', {}).get('abbreviation', '')
        
        return [{
            'name': name,
            'position': position,
            'recent_stats': "No recent data"
        }]
    

        
        