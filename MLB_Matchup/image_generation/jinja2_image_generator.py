import os
import json
import sys
import urllib.request
import base64
from concurrent.futures import ThreadPoolExecutor

# Add src directory to path for MLB_API_Client
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'utils'))

from jinja2 import Template
from MLB_API_Client import MLBAPIClient
import get_address
from html_to_image_converter import convert_html_string_to_image_sync

class Jinja2ImageGenerator:
    def __init__(self):
        self.mlb_client = MLBAPIClient()
        self.config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config')
        
        # Load team data
        self.team_abbreviations = self.load_team_abbreviations()
        self.team_colors = self.load_team_colors()
        
    def load_team_abbreviations(self):
        """Load team abbreviations from JSON file"""
        try:
            config_path = os.path.join(self.config_path, 'teamAbreviations.json')
            with open(config_path, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading team abbreviations: {e}")
            return {}
    
    def load_team_colors(self):
        """Load team colors from JSON file"""
        try:
            config_path = os.path.join(self.config_path, 'teamPrimaryColors.json')
            with open(config_path, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading team colors: {e}")
            return {}
    
    def load_team_secondary_colors(self):
        """Load team secondary colors from JSON file"""
        try:
            config_path = os.path.join(self.config_path, 'teamSecondaryColors.json')
            with open(config_path, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading team secondary colors: {e}")
            return {}
    
    def load_anton_font(self):
        """Load Anton font base64 data"""
        try:
            config_path = os.path.join(self.config_path, 'anton.ttf.base64.txt')
            with open(config_path, "r") as f:
                return f.read().strip()
        except Exception as e:
            print(f"Error loading Anton font: {e}")
            return ""
    
    def load_worksans_regular_font(self):
        """Load WorkSans-Regular font base64 data"""
        try:
            config_path = os.path.join(self.config_path, 'WorkSans-Regular.ttf.base64.txt')
            with open(config_path, "r") as f:
                return f.read().strip()
        except Exception as e:
            print(f"Error loading WorkSans-Regular font: {e}")
            return ""
    
    def load_worksans_bold_font(self):
        """Load WorkSans-Bold font base64 data"""
        try:
            config_path = os.path.join(self.config_path, 'WorkSans-Bold.ttf.base64.txt')
            with open(config_path, "r") as f:
                return f.read().strip()
        except Exception as e:
            print(f"Error loading WorkSans-Bold font: {e}")
            return ""
    
    def build_headshot_url(self, player_id):
        """Build MLB official headshot URL for a player ID"""
        if not player_id:
            return ""
        return (
            f"https://img.mlbstatic.com/mlb-photos/image/upload/"
            f"d_people:generic:headshot:67:current.png/w_180,q_auto:best/"
            f"v1/people/{player_id}/headshot/67/current"
        )

    def fetch_headshot_b64(self, player_id):
        """Download a player headshot and return it as a base64 data URI.
        Playwright blocks external URLs when rendering via set_content(),
        so images must be embedded directly in the HTML."""
        if not player_id:
            return ""
        url = self.build_headshot_url(player_id)
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=8) as response:
                image_data = response.read()
                content_type = response.headers.get('Content-Type', 'image/png').split(';')[0]
                b64 = base64.b64encode(image_data).decode('utf-8')
                return f"data:{content_type};base64,{b64}"
        except Exception as e:
            print(f"Could not load headshot for player {player_id}: {e}")
            return ""

    def fetch_headshots_parallel(self, player_ids):
        """Fetch multiple headshots concurrently. Returns {player_id: data_uri}."""
        unique_ids = list({pid for pid in player_ids if pid})
        if not unique_ids:
            return {}
        print(f"Fetching {len(unique_ids)} player headshots...")
        with ThreadPoolExecutor(max_workers=12) as executor:
            results = list(executor.map(self.fetch_headshot_b64, unique_ids))
        return dict(zip(unique_ids, results))

    def get_team_abbreviation(self, team_name):
        """Get team abbreviation from full team name"""
        return self.team_abbreviations.get(team_name, team_name[:3].upper())
    
    def format_player_stats(self, stats_string):
        """Format player stats for display"""
        if stats_string == "No recent data":
            return "No recent data"
        
        # Parse the existing stats format and make it more readable
        try:
            # Extract key stats and format them nicely
            if "AVG:" in stats_string and "OPS:" in stats_string:
                # Format: "AVG: 0.300 / OPS: 0.850 / H: 15 / RBIs: 8 / SO: 12"
                return stats_string.replace(" / ", " | ")
            else:
                return stats_string
        except:
            return stats_string
    
    def format_pitcher_stats(self, stats_string):
        """Format pitcher stats for display"""
        if stats_string == "No recent data":
            return "No recent data"
        
        # Parse the existing pitcher stats format
        try:
            if "ERA:" in stats_string and "WHIP:" in stats_string:
                # Format: "ERA: 3.50 WHIP: 1.25 K: 45 IP: 60.2"
                # Convert to: "ERA: 3.50 | WHIP: 1.25 | K: 45 | IP: 60.2"
                return stats_string.replace(" WHIP:", " | WHIP:").replace(" K:", " | K:").replace(" IP:", " | IP:")
            else:
                return stats_string
        except:
            return stats_string
    
    def prepare_template_data(self, game_data):
        """Prepare data structure for Jinja2 template"""
        try:
            # Load font base64 data
            anton_font_b64 = self.load_anton_font()
            worksans_regular_font_b64 = self.load_worksans_regular_font()
            worksans_bold_font_b64 = self.load_worksans_bold_font()
            
            # Extract basic game info
            away_team = game_data.get('away_team', 'Unknown')
            home_team = game_data.get('home_team', 'Unknown')
            game_date = game_data.get('game_date', 'Unknown')
            game_time = game_data.get('game_time', 'Unknown')
            game_location = game_data.get('game_location', 'Unknown')
            
            # Get team records
            away_record = self.mlb_client.get_team_record(away_team)
            home_record = self.mlb_client.get_team_record(home_team)
            
            # Get team abbreviations
            away_abbrev = self.get_team_abbreviation(away_team)
            home_abbrev = self.get_team_abbreviation(home_team)
            
            # Get team colors
            team_primary_colors = self.load_team_colors()
            team_secondary_colors = self.load_team_secondary_colors()
            
            away_primary_color = team_primary_colors.get(away_team, '#00385D')
            away_secondary_color = team_secondary_colors.get(away_team, '#e50022')
            home_primary_color = team_primary_colors.get(home_team, '#002D72')
            home_secondary_color = team_secondary_colors.get(home_team, '#FF5910')
            
            # Get raw pitcher and lineup data
            away_pitcher_raw = game_data.get('away_pitcher', {})
            away_pitcher_id = away_pitcher_raw.get('player_id')
            home_pitcher_raw = game_data.get('home_pitcher', {})
            home_pitcher_id = home_pitcher_raw.get('player_id')
            away_players = game_data.get('away_lineup', [])
            home_players = game_data.get('home_lineup', [])

            # Collect all player IDs and fetch headshots in parallel (base64 so
            # Playwright can embed them without making external network requests)
            all_ids = ([p.get('player_id') for p in away_players + home_players]
                       + [away_pitcher_id, home_pitcher_id])
            headshot_map = self.fetch_headshots_parallel(all_ids)

            # Build pitcher dicts
            away_pitcher = {
                'name': away_pitcher_raw.get('name', 'TBD'),
                'position': away_pitcher_raw.get('position', 'P'),
                'stats': self.format_pitcher_stats(away_pitcher_raw.get('stats', 'No recent data')),
                'player_id': away_pitcher_id,
                'headshot_b64': headshot_map.get(away_pitcher_id, '')
            }
            home_pitcher = {
                'name': home_pitcher_raw.get('name', 'TBD'),
                'position': home_pitcher_raw.get('position', 'P'),
                'stats': self.format_pitcher_stats(home_pitcher_raw.get('stats', 'No recent data')),
                'player_id': home_pitcher_id,
                'headshot_b64': headshot_map.get(home_pitcher_id, '')
            }

            # Process lineups, passing the pre-fetched headshot map
            away_lineup = self.process_lineup_single_pass(away_players, game_data.get('away_team', ''), headshot_map)
            home_lineup = self.process_lineup_single_pass(home_players, game_data.get('home_team', ''), headshot_map)
            
            # Return template data
            return {
                'anton_font_b64': anton_font_b64,
                'worksans_regular_font_b64': worksans_regular_font_b64,
                'worksans_bold_font_b64': worksans_bold_font_b64,
                'away_team_abbrev': away_abbrev,
                'home_team_abbrev': home_abbrev,
                'away_team_record': away_record.get('record', '0-0'),
                'home_team_record': home_record.get('record', '0-0'),
                'game_date': game_date,
                'game_time': game_time,
                'game_location': game_location,
                'away_pitcher': away_pitcher,
                'home_pitcher': home_pitcher,
                'away_lineup': away_lineup,
                'home_lineup': home_lineup,
                'away_primary_color': away_primary_color,
                'away_secondary_color': away_secondary_color,
                'home_primary_color': home_primary_color,
                'home_secondary_color': home_secondary_color
            }
            
        except Exception as e:
            print(f"Error preparing template data: {e}")
            return {}
    
    def get_team_id_from_name(self, team_name):
        """Get team ID from team name for statsapi lookup"""
        # Team name to ID mapping (you can expand this)
        team_id_map = {
            'Los Angeles Dodgers': 119,
            'New York Yankees': 147,
            'Boston Red Sox': 111,
            'Chicago Cubs': 112,
            'San Francisco Giants': 137,
            'St. Louis Cardinals': 138,
            'Atlanta Braves': 144,
            'Houston Astros': 117,
            'Toronto Blue Jays': 141,
            'Seattle Mariners': 136,
            'Texas Rangers': 140,
            'Baltimore Orioles': 110,
            'Tampa Bay Rays': 139,
            'Cleveland Guardians': 114,
            'Minnesota Twins': 142,
            'Detroit Tigers': 116,
            'Kansas City Royals': 118,
            'Chicago White Sox': 145,
            'Oakland Athletics': 133,
            'Athletics': 133,  # Alternative name
            'Los Angeles Angels': 108,
            'Arizona Diamondbacks': 109,
            'Colorado Rockies': 115,
            'San Diego Padres': 135,
            'Milwaukee Brewers': 158,
            'Cincinnati Reds': 113,
            'Pittsburgh Pirates': 134,
            'Philadelphia Phillies': 143,
            'New York Mets': 121,
            'Washington Nationals': 120,
            'Miami Marlins': 146
        }
        
        # Debug: Print team name lookup
        team_id = team_id_map.get(team_name, 119)  # Default to Dodgers if not found
        if team_id == 119 and team_name not in team_id_map:
            print(f"⚠️ Warning: Team '{team_name}' not found in team_id_map, defaulting to Dodgers (ID: 119)")
        else:
            print(f"✅ Team '{team_name}' -> ID {team_id}")
        
        return team_id
    
    def process_lineup_single_pass(self, players, team_name, headshot_map=None):
        """Process entire lineup in a single pass - with OPS trends for color coding"""
        try:
            if not players:
                return []

            if headshot_map is None:
                headshot_map = {}

            processed_lineup = []

            # Process each player exactly once - get OPS trend for color coding
            for player in players:
                player_name = player.get('name', 'TBD')
                position = player.get('position', '')
                stats = self.format_player_stats(player.get('stats', 'No recent data'))
                ops_trend = player.get('ops_trend', 'neutral')
                player_id = player.get('player_id')

                # Debug: Print the ops_trend values being processed
                print(f"🔍 DEBUG - Player: {player_name}, OPS Trend: '{ops_trend}' (type: {type(ops_trend)})")

                # Add player to lineup with OPS trend for color coding
                processed_lineup.append({
                    'name': player_name,
                    'position': position,
                    'stats': stats,
                    'ops_trend': ops_trend,
                    'player_id': player_id,
                    'headshot_b64': headshot_map.get(player_id, '')
                })
            
            return processed_lineup
                
        except Exception as e:
            print(f"Error processing lineup: {e}")
            return []
    
    def render_template(self, template_path, data):
        """Render Jinja2 template with data"""
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            template = Template(template_content)
            rendered_html = template.render(**data)
            return rendered_html
            
        except Exception as e:
            print(f"Error rendering template: {e}")
            return None
    
    def create_lineup_image(self, game_data, output_path):
        """Create lineup image using Jinja2 template and convert to PNG"""
        try:
            # Prepare data for template
            template_data = self.prepare_template_data(game_data)
            
            if not template_data:
                print("Failed to prepare template data")
                return False
            
            # Get template path
            template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'image_generator_v3.html')
            
            # Render template
            rendered_html = self.render_template(template_path, template_data)
            
            if not rendered_html:
                print("Failed to render template")
                return False
            
            print(f"✅ Template rendered successfully with {len(template_data)} variables")
            
            # Convert HTML to image using Playwright
            print("🖼️  Converting HTML to image...")
            success = convert_html_string_to_image_sync(rendered_html, output_path)
            
            if success:
                print(f"✅ Lineup image created successfully at: {output_path}")
                return True
            else:
                print("❌ Failed to convert HTML to image")
                return False
            
        except Exception as e:
            print(f"Error creating lineup image: {e}")
            return False
    
    def create_lineup_from_game_id(self, game_id, output_path):
        """Create lineup image from MLB game ID"""
        try:
            # Get game data from MLB API
            boxscore = self.mlb_client.get_boxscore(game_id)
            
            if not boxscore:
                print(f"Failed to get boxscore for game {game_id}")
                return False
            
            # Extract game info
            game_info = self.extract_game_info(boxscore)
            
            # Extract lineups
            away_lineup = self.mlb_client.extract_lineup_data(boxscore, 'away')
            home_lineup = self.mlb_client.extract_lineup_data(boxscore, 'home')
            
            # Extract pitchers
            away_pitcher = self.mlb_client.extract_pitcher_data(boxscore, 'away')
            home_pitcher = self.mlb_client.extract_pitcher_data(boxscore, 'home')
            
            # Prepare game data
            game_data = {
                'away_team': game_info['away_team'],
                'home_team': game_info['home_team'],
                'game_date': game_info['game_date'],
                'game_time': game_info['game_time'],
                'game_venue': game_info['game_venue'],
                'game_location': game_info['game_location'],
                'away_lineup': away_lineup,
                'home_lineup': home_lineup,
                'away_pitcher': away_pitcher[0] if away_pitcher else {},
                'home_pitcher': home_pitcher[0] if home_pitcher else {}
            }
            
            # Create image
            return self.create_lineup_image(game_data, output_path)
            
        except Exception as e:
            print(f"Error creating lineup from game ID: {e}")
            return False
    
    def extract_game_info(self, boxscore):
        """Extract basic game information from boxscore"""
        try:
            # Get teams
            away_team = boxscore.get('away', {}).get('team', {}).get('name', 'Unknown')
            home_team = boxscore.get('home', {}).get('team', {}).get('name', 'Unknown')
            
            # Get game date and time
            game_datetime = boxscore.get('gameData', {}).get('datetime', {}).get('officialDate', '')
            game_time = boxscore.get('gameData', {}).get('datetime', {}).get('time', {}).get('time', '')
            
            # Format date and time
            formatted_date, formatted_time = self.mlb_client.format_game_datetime(game_datetime, game_datetime)
            
            # Get venue location
            venue_id = boxscore.get('gameData', {}).get('venue', {}).get('id')
            venue_data = self.mlb_client.get_venue_data(venue_id)
            game_location = self.mlb_client.get_venue_location(venue_data.get('name', 'Unknown')) if venue_data else 'Unknown'
            
            return {
                'away_team': away_team,
                'home_team': home_team,
                'game_date': formatted_date,
                'game_time': formatted_time,
                'game_location': game_location
            }
            
        except Exception as e:
            print(f"Error extracting game info: {e}")
            return {
                'away_team': 'Unknown',
                'home_team': 'Unknown',
                'game_date': 'Unknown',
                'game_time': 'Unknown',
                'game_location': 'Unknown'
            }


# Example usage function
def create_lineup_image_example():
    """Example of how to use the Jinja2ImageGenerator"""
    generator = Jinja2ImageGenerator()
    
    # Example game data (you would normally get this from MLB API)
    example_game_data = {
        'away_team': 'Pittsburgh Pirates',
        'home_team': 'Cleveland Guardians',
        'game_date': '08/04/2025',
        'game_time': '7:05 PM ET',
        'game_location': 'Yankee Stadium',
        'away_pitcher': {
            'name': 'Seth Lugo',
            'position': 'P',
            'stats': 'ERA: 3.45 | WHIP: 1.15 | K: 156 | IP: 180.1'
        },
        'home_pitcher': {
            'name': 'Gerrit Cole',
            'position': 'P',
            'stats': 'ERA: 2.95 | WHIP: 1.08 | K: 178 | IP: 185.2'
        },
        'away_lineup': [
            {'name': 'Pete Crow-Amrstrong', 'position': 'CF', 'stats': 'AVG: .298 | OPS: .812 | H: 89 | HR: 8 | SO: 67 | RBI: 45', 'ops_trend': 'hot'},
            {'name': 'Christian Encarnacion-Strand', 'position': '3B', 'stats': 'AVG: .275 | OPS: .890 | H: 102 | HR: 25 | SO: 89 | RBI: 78'},
            {'name': 'Triston Casas', 'position': '1B', 'stats': 'AVG: .263 | OPS: .856 | H: 76 | HR: 18 | SO: 82 | RBI: 52'},
            {'name': 'Masataka Yoshida', 'position': 'LF', 'stats': 'AVG: .289 | OPS: 1.283 | H: 95 | HR: 12 | SO: 58 | RBI: 61'},
            {'name': 'Connor Wong', 'position': 'C', 'stats': 'AVG: .245 | OPS: .712 | H: 67 | HR: 9 | SO: 71 | RBI: 38'},
            {'name': 'Pablo Reyes', 'position': '2B', 'stats': 'AVG: .271 | OPS: .734 | H: 58 | HR: 6 | SO: 45 | RBI: 32'},
            {'name': 'Ceddanne Rafaela', 'position': 'SS', 'stats': 'AVG: .234 | OPS: .678 | H: 43 | HR: 5 | SO: 52 | RBI: 28'},
            {'name': 'Wilyer Abreu', 'position': 'RF', 'stats': 'AVG: .256 | OPS: .745 | H: 51 | HR: 7 | SO: 48 | RBI: 35'},
            {'name': 'Wilyer Abreu', 'position': 'RF', 'stats': 'AVG: .256 | OPS: .745 | H: 51 | HR: 7 | SO: 48 | RBI: 35'}
        ],
        'home_lineup': [
            {'name': 'DJ LeMahieu', 'position': '3B', 'stats': 'AVG: .267 | OPS: .745 | H: 78 | HR: 12 | SO: 62 | RBI: 48', 'ops_trend': 'hot'},
            {'name': 'Aaron Judge', 'position': 'CF', 'stats': 'AVG: .291 | OPS: .987 | H: 89 | HR: 32 | SO: 79 | RBI: 78', 'ops_trend': 'cold'},
            {'name': 'Giancarlo Stanton', 'position': 'DH', 'stats': 'AVG: .245 | OPS: .785 | H: 67 | HR: 18 | SO: 85 | RBI: 52'},
            {'name': 'Anthony Rizzo', 'position': '1B', 'stats': 'AVG: .278 | OPS: .812 | H: 82 | HR: 15 | SO: 71 | RBI: 58'},
            {'name': 'Gleyber Torres', 'position': '2B', 'stats': 'AVG: .263 | OPS: .756 | H: 89 | HR: 14 | SO: 68 | RBI: 62'},
            {'name': 'Austin Wells', 'position': 'C', 'stats': 'AVG: .234 | OPS: .678 | H: 45 | HR: 8 | SO: 52 | RBI: 31'},
            {'name': 'Oswaldo Cabrera', 'position': 'LF', 'stats': 'AVG: .256 | OPS: .712 | H: 58 | HR: 9 | SO: 48 | RBI: 38'},
            {'name': 'Anthony Volpe', 'position': 'SS', 'stats': 'AVG: .245 | OPS: .734 | H: 67 | HR: 11 | SO: 71 | RBI: 42'},
            {'name': 'Gerrit Cole', 'position': 'P', 'stats': 'ERA: 2.95 | WHIP: 1.08 | K: 178 | IP: 185.2'}
        ]
    }
    
    # Create the image
    output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'images', 'jinja2_example_lineup.png')
    success = generator.create_lineup_image(example_game_data, output_path)
    
    if success:
        print(f"✅ Lineup image created successfully at: {output_path}")
    else:
        print("❌ Failed to create lineup image")
    
    return success


if __name__ == "__main__":
    create_lineup_image_example()
