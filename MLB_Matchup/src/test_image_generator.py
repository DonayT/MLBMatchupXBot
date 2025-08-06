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
from game_data_processor import GameDataProcessor
from MLB_API_Client import MLBAPIClient

def get_real_game_data():
    """Get real game data from MLB API using modularized code"""
    try:
        api_client = MLBAPIClient()
        game_processor = GameDataProcessor()
        
        # Get today's schedule
        schedule = api_client.get_schedule()
        
        if len(schedule) == 0:
            return None
        
        # Get the first game with official lineups
        for game in schedule:
            game_data = game_processor.get_game_data(game)
            
            if game_data['lineups_official']:
                return game_data
        
        return None
        
    except Exception as e:
        print(f"Error getting real game data: {e}")
        return None

def create_test_image():
    """Generate a test lineup image with real or mock data"""
    
    # Try to get real game data first
    test_data = get_real_game_data()
    
    if test_data is None:
        print("No real games with official lineups found, using mock data")
        test_data = create_mock_game_data()
    
    try:
        # Generate the image in test mode
        image_path = create_twitter_image(test_data, test_mode=True)
        
        if image_path:
            print(f"Test image created successfully: {image_path}")
        else:
            print("Failed to create test image")
        
        return image_path
        
    except Exception as e:
        print(f"Error creating test image: {e}")
        return None

def main():
    """Main function to run the test image generator"""
    
    print("Starting test image generation...")
    
    # Generate test image
    image_path = create_test_image()
    
    if image_path:
        print("Test completed successfully!")
        return 0
    else:
        print("Test failed!")
        return 1

if __name__ == "__main__":
    exit(main()) 