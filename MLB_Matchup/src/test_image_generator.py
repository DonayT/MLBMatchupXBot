#!/usr/bin/env python3
"""
Test Image Generator for MLB Lineup Bot
This script generates a single lineup image using real MLB API data.
It gets the first available game with official lineups, or falls back to mock data.
"""

import os
import sys
from datetime import datetime

# Add the src directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from twitter_image_generator import create_twitter_image
import statsapi
import pprint

def are_lineups_official(boxscore):
    """Check if both home and away lineups are official"""
    home_batting_order = boxscore['home'].get('battingOrder', [])
    away_batting_order = boxscore['away'].get('battingOrder', [])
    
    # Lineups are official if both teams have batting orders with at least 9 players
    return len(home_batting_order) >= 9 and len(away_batting_order) >= 9

def get_game_data(game):
    """Extract all relevant game data for image generation"""
    game_id = game['game_id']
    home = game['home_name']
    away = game['away_name']
    
    boxscore = statsapi.boxscore_data(game_id)
    
    home_pitcher = game.get('home_probable_pitcher') or 'TBD'
    away_pitcher = game.get('away_probable_pitcher') or 'TBD'
    
    # Get game date and time
    game_datetime = game.get('game_datetime', '')
    game_date = game.get('game_date', '')

    venue_id = game.get('venue_id')
    venue_name = 'Unknown Venue'
    city = 'Unknown City'
    state = 'Unknown State'

    if venue_id:
        venue_data = statsapi.get('venue', {'venueIds': venue_id})
        venue = venue_data['venues'][0]
        venue_name = venue.get('name', 'Unknown Venue')
        city = venue.get('city', 'Unknown')
        state = venue.get('state', 'Unknown')

    # Format the date and time separately
    if game_datetime:
        try:
            # Parse the datetime string and format it
            from datetime import datetime
            from zoneinfo import ZoneInfo

            #Switch to Eastern Time
            dt = datetime.fromisoformat(game_datetime.replace('Z', '+00:00'))
            dt_et = dt.astimezone(ZoneInfo("America/New_York"))

            #Format date/time
            formatted_date = dt_et.strftime('%m/%d/%Y')
            formatted_time = dt_et.strftime('%I:%M %p ET')
        except:
            formatted_date = game_date if game_date else 'TBD'
            formatted_time = 'TBD'
    else:
        formatted_date = game_date if game_date else 'TBD'
        formatted_time = 'TBD'
    
    game_data = {
        'game_id': game_id,
        'home_team': home,
        'away_team': away,
        'home_pitcher': home_pitcher,
        'away_pitcher': away_pitcher,
        'game_date': formatted_date,
        'game_time': formatted_time,
        'home_lineup': [],
        'away_lineup': [],
        'venue': venue_name,
        'city': city,
        'state': state,
        'lineups_official': are_lineups_official(boxscore)
    }
    
    # Extract lineups if they exist
    for side in ['home', 'away']:
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
        
        if side == 'home':
            game_data['home_lineup'] = lineup
        else:
            game_data['away_lineup'] = lineup
    
    return game_data

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

def get_real_game_data():
    """Get real game data from MLB API"""
    try:
        # Get today's schedule
        today = datetime.now().strftime('%Y-%m-%d')
        schedule = statsapi.schedule(start_date=today, end_date=today)
        
        if len(schedule) == 0:
            return None
        
        # Get the first game with official lineups
        for game in schedule:
            game_data = get_game_data(game)
            
            if game_data['lineups_official']:
                return game_data
        
        return None
        
    except Exception as e:
        return None

def create_test_image():
    """Generate a test lineup image with real or mock data"""
    
    # Try to get real game data first
    test_data = get_real_game_data()
    
    if test_data is None:
        test_data = create_mock_game_data()
    
    try:
        # Generate the image in test mode
        image_path = create_twitter_image(test_data, test_mode=True)
        
        return image_path
        
    except Exception as e:
        return None

def main():
    """Main function to run the test image generator"""
    
    # Generate test image
    image_path = create_test_image()
    
    if not image_path:
        sys.exit(1)

if __name__ == "__main__":
    main() 