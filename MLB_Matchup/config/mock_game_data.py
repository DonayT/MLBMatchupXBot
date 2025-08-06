"""
Mock Game Data Module
Provides sample game data for testing when no real games are available
"""
import sys
import os

# Add the config directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def create_mock_game_data():
    """Create sample game data for testing when no real games are available"""
    
    # Sample game data structure
    test_game_data = {
        'game_id': '123456',
        'home_team': 'New York Yankees',
        'away_team': 'Boston Red Sox',
        'home_pitcher': 'Gerrit Cole',
        'away_pitcher': 'Chris Sale',
        'game_date': '08/04/2025',
        'game_time': '7:05 PM ET',
        'venue': 'Yankee Stadium',
        'city': 'Bronx',
        'state': 'NY',
        'lineups_official': True,
        
        # Sample away team lineup (Red Sox)
        'away_lineup': [
            {'order': 1, 'name': 'Jarren Duran', 'position': 'CF'},
            {'order': 2, 'name': 'Rafael Devers', 'position': '3B'},
            {'order': 3, 'name': 'Triston Casas', 'position': '1B'},
            {'order': 4, 'name': 'Masataka Yoshida', 'position': 'LF'},
            {'order': 5, 'name': 'Connor Wong', 'position': 'C'},
            {'order': 6, 'name': 'Enmanuel Valdez', 'position': '2B'},
            {'order': 7, 'name': 'Wilyer Abreu', 'position': 'RF'},
            {'order': 8, 'name': 'Pablo Reyes', 'position': 'SS'},
            {'order': 9, 'name': 'Ceddanne Rafaela', 'position': 'DH'}
        ],
        
        # Sample home team lineup (Yankees)
        'home_lineup': [
            {'order': 1, 'name': 'DJ LeMahieu', 'position': '3B'},
            {'order': 2, 'name': 'Aaron Judge', 'position': 'RF'},
            {'order': 3, 'name': 'Anthony Rizzo', 'position': '1B'},
            {'order': 4, 'name': 'Giancarlo Stanton', 'position': 'DH'},
            {'order': 5, 'name': 'Gleyber Torres', 'position': '2B'},
            {'order': 6, 'name': 'Austin Wells', 'position': 'C'},
            {'order': 7, 'name': 'Oswaldo Cabrera', 'position': 'LF'},
            {'order': 8, 'name': 'Anthony Volpe', 'position': 'SS'},
            {'order': 9, 'name': 'Jasson Dominguez', 'position': 'CF'}
        ]
    }
    
    return test_game_data