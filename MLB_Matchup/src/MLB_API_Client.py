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
                lineup.append({
                    'order': idx,
                    'name': name,
                    'position': position
                })
        
        return lineup
    
    def are_lineups_official(self, boxscore):
        return self.lineup_validator.are_lineups_official(boxscore)
        
        