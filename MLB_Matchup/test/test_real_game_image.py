#!/usr/bin/env python3
"""
Test Real Game Image Generation
This script tests the new Jinja2-based image generation system with real MLB game data.
It finds the first official game and creates a lineup image using actual player stats.
"""

import sys
import os
import json
from datetime import datetime

# Add the src directory to the path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from jinja2_image_generator import Jinja2ImageGenerator
from MLB_API_Client import MLBAPIClient
from game_data_processor import GameDataProcessor

def test_real_game_image():
    """Test image generation with real MLB game data"""
    print("🧪 Testing Real Game Image Generation with Jinja2")
    print("=" * 60)
    
    try:
        # Initialize the components
        print("📡 Initializing MLB API Client...")
        mlb_client = MLBAPIClient()
        
        print("🎨 Initializing Jinja2 Image Generator...")
        jinja2_generator = Jinja2ImageGenerator()
        
        print("⚙️  Initializing Game Data Processor...")
        game_processor = GameDataProcessor()
        
        # Get today's schedule
        today = datetime.now().strftime('%Y-%m-%d')
        print(f"\n📅 Getting schedule for {today}...")
        
        schedule = mlb_client.get_schedule(date=today)
        
        if not schedule:
            print("❌ No games found for today")
            return False
            
        print(f"🏟️  Found {len(schedule)} games today")
        
        # Debug: Show the structure of the first game
        if schedule:
            print(f"\n🔍 Debug - First game structure:")
            first_game = schedule[0]
            print(f"   Available keys: {list(first_game.keys())}")
            print(f"   First game data: {first_game}")
        
        # Find the first game with official lineups
        official_game = None
        for game in schedule:
            # Use the correct keys based on statsapi structure
            away_team = game.get('away_name', game.get('away_team', 'Unknown'))
            home_team = game.get('home_name', game.get('home_team', 'Unknown'))
            game_id = game.get('game_id', game.get('game_pk', 'Unknown'))
            
            print(f"\n🔍 Checking game: {away_team} @ {home_team} (ID: {game_id})")
            
            # Get detailed game data
            game_data = game_processor.get_game_data(game)
            
            print(f"   📊 Lineups Official: {game_data['lineups_official']}")
            print(f"   🏠 Home Team: {game_data['home_team']}")
            print(f"   ✈️  Away Team: {game_data['away_team']}")
            
            if game_data['lineups_official']:
                print(f"   ✅ Found official game: {game_data['away_team']} @ {game_data['home_team']}")
                official_game = game_data
                break
            else:
                print(f"   ⏳ Waiting for lineups to become official...")
        
        if not official_game:
            print("\n❌ No games with official lineups found today")
            print("💡 Try running this test when games are closer to start time")
            return False
        
        # Now create the image with real data
        print(f"\n🎨 Creating lineup image for official game...")
        print(f"   Game: {official_game['away_team']} @ {official_game['home_team']}")
        print(f"   Game ID: {official_game['game_id']}")
        print(f"   Date: {official_game['game_date']}")
        print(f"   Time: {official_game['game_time']}")
        
        # Show some sample data that will be used
        print(f"\n📊 Sample Player Data:")
        if official_game['away_lineup']:
            first_player = official_game['away_lineup'][0]
            print(f"   Away Player 1: {first_player.get('name', 'N/A')} - {first_player.get('position', 'N/A')}")
            print(f"   Stats: {first_player.get('recent_stats', 'No stats')[:100]}...")
        
        if official_game['home_lineup']:
            first_player = official_game['home_lineup'][0]
            print(f"   Home Player 1: {first_player.get('name', 'N/A')} - {first_player.get('position', 'N/A')}")
            print(f"   Stats: {first_player.get('recent_stats', 'No stats')[:100]}...")
        
        # Create the output path
        test_images_dir = os.path.join(os.path.dirname(__file__), 'testImages')
        os.makedirs(test_images_dir, exist_ok=True)
        
        away_team_clean = official_game['away_team'].replace(' ', '_').replace('.', '')
        home_team_clean = official_game['home_team'].replace(' ', '_').replace('.', '')
        game_id = official_game['game_id']
        
        output_filename = f"REAL_TEST_lineup_{away_team_clean}_vs_{home_team_clean}_{game_id}.png"
        output_path = os.path.join(test_images_dir, output_filename)
        
        print(f"\n🖼️  Output path: {output_path}")
        print(f"   📁 Saving to testImages folder for testing purposes")
        
        # Format the game data to match what Jinja2ImageGenerator expects
        formatted_away_lineup = []
        for player in official_game['away_lineup']:
            formatted_away_lineup.append({
                'name': player.get('name', 'TBD'),
                'position': player.get('position', ''),
                'stats': player.get('recent_stats', 'No recent data'),  # Map recent_stats to stats
                'ops_trend': player.get('ops_trend', 'neutral')  # Preserve OPS trend for color coding
            })
        
        formatted_home_lineup = []
        for player in official_game['home_lineup']:
            formatted_home_lineup.append({
                'name': player.get('name', 'TBD'),
                'position': player.get('position', ''),
                'stats': player.get('recent_stats', 'No recent data'),  # Map recent_stats to stats
                'ops_trend': player.get('ops_trend', 'neutral')  # Preserve OPS trend for color coding
            })
        
        formatted_game_data = {
            'away_team': official_game['away_team'],
            'home_team': official_game['home_team'],
            'game_date': official_game['game_date'],
            'game_time': official_game['game_time'],
            'game_location': official_game['venue'],  # Just show stadium name
            'away_lineup': formatted_away_lineup,
            'home_lineup': formatted_home_lineup,
            'away_pitcher': {
                'name': official_game['away_pitcher'] if official_game['away_pitcher'] != 'TBD' else 'TBD',
                'position': 'P',
                'stats': official_game['away_pitchers'][0].get('recent_stats', 'No recent data') if official_game['away_pitchers'] else 'No recent data'
            },
            'home_pitcher': {
                'name': official_game['home_pitcher'] if official_game['home_pitcher'] != 'TBD' else 'TBD',
                'position': 'P',
                'stats': official_game['home_pitchers'][0].get('recent_stats', 'No recent data') if official_game['home_pitchers'] else 'No recent data'
            }
        }
        
        # Generate the image
        print(f"\n🚀 Generating image with Jinja2...")
        success = jinja2_generator.create_lineup_image(formatted_game_data, output_path)
        
        if success:
            print(f"\n✅ SUCCESS! Real game lineup image created!")
            print(f"   📁 Image saved to: {output_filename}")
            print(f"   🎯 This proves your Jinja2 system works with real MLB data!")
            
            return True
        else:
            print(f"\n❌ Failed to create image")
            return False
            
    except Exception as e:
        print(f"\n💥 Error during real game image test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🧪 REAL GAME IMAGE GENERATION TEST")
    print("=" * 50)
    print("This test will:")
    print("1. Find the first MLB game with official lineups today")
    print("2. Extract real player stats and lineup data")
    print("3. Generate a lineup image using your new Jinja2 system")
    print("4. Save the image to the testImages folder")
    print("=" * 50)
    
    success = test_real_game_image()
    
    if success:
        print("\n🎉 TEST PASSED! Your Jinja2 system is working with real MLB data!")
        print("💡 You can now run Main.py to process all games automatically!")
    else:
        print("\n❌ TEST FAILED! Check the error messages above.")
    
    return success

if __name__ == "__main__":
    main()
