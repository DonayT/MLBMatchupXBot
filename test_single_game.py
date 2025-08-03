#!/usr/bin/env python3
"""
Test script for single game with new modern layout and performance indicators
"""
import sys
import os
sys.path.append('MLB_Matchup/src')

from MLBMatchup import get_game_data
import statsapi
from datetime import datetime
from twitter_image_generator import create_twitter_image

def test_single_game():
    """Test the new modern layout system with one game from today"""
    
    print("🎯 Testing Modern MLB Lineup Generator")
    print("=" * 50)
    
    # Get today's games
    today = datetime.now().strftime('%Y-%m-%d')
    print(f"📅 Getting games for {today}...")
    
    try:
        schedule = statsapi.schedule(start_date=today, end_date=today)
        
        if not schedule:
            print("❌ No games found for today")
            return False
            
        print(f"📊 Found {len(schedule)} games today")
        
        # Show available games
        print("\nAvailable games:")
        for i, game in enumerate(schedule[:5]):  # Show first 5
            status = game.get('status', 'Unknown')
            print(f"  {i+1}. {game['away_name']} @ {game['home_name']} ({status})")
        
        # Take first game
        game = schedule[0]
        print(f"\n🎮 Testing: {game['away_name']} @ {game['home_name']}")
        
        # Get game data with pybaseball stats
        print("📈 Fetching game data and player stats...")
        game_data = get_game_data(game)
        
        print(f"   Lineups Official: {game_data['lineups_official']}")
        print(f"   Away Pitcher: {game_data['away_pitcher']}")
        print(f"   Home Pitcher: {game_data['home_pitcher']}")
        
        # Generate modern image
        print("🎨 Generating modern lineup image...")
        image_path = create_twitter_image(game_data)
        
        print("\n" + "=" * 50)
        print("✅ SUCCESS!")
        print(f"📁 Generated: {image_path}")
        print("\n🎯 New Features:")
        print("🔥 RED outlines = Hot players (recent good performance)")
        print("🧊 BLUE outlines = Cold players (recent poor performance)")
        print("⚪ No outline = Neutral players (.250-.300 range)")
        print("📊 Clean layout with no commas in stats")
        print("🎪 Modern design with performance indicators")
        
        # Check file exists
        if os.path.exists(image_path):
            file_size = os.path.getsize(image_path) / 1024
            print(f"📏 File size: {file_size:.1f} KB")
            return True
        else:
            print("❌ Error: Image file not found")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_single_game()
    if success:
        print("\n🎉 Test completed successfully!")
    else:
        print("\n💥 Test failed!")