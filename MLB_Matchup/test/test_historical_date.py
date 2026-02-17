"""
Test script to run the bot for a specific historical date
This allows testing with real game data from past seasons and generates lineup cards
"""

import statsapi
from datetime import datetime
import time
import os
import sys

# Add src, utils, and image_generation directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'utils'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'image_generation'))

from MLB_API_Client import MLBAPIClient
from game_data_processor import GameDataProcessor
from jinja2_image_generator import Jinja2ImageGenerator
from api_cache import get_cache

def test_historical_date(date_str, generate_images=True):
    """
    Run the bot for a specific historical date to see optimization in action
    and generate lineup card images

    params: date_str (str) - Date in YYYY-MM-DD format (e.g., "2025-08-08")
            generate_images (bool) - Whether to generate lineup card images (default: True)
    """
    print("=" * 80)
    print(f"Testing MLBMatchupXBot for historical date: {date_str}")
    print("=" * 80)
    print()

    # Clear cache to start fresh
    cache = get_cache()
    cache.clear()

    # Fetch schedule for the specified date
    print(f"📅 Fetching MLB schedule for {date_str}...")
    schedule = statsapi.schedule(start_date=date_str, end_date=date_str)

    if not schedule:
        print(f"❌ No games found for {date_str}")
        return

    print(f"✅ Found {len(schedule)} games on {date_str}")
    print()

    # Initialize components
    mlb_client = MLBAPIClient()
    game_processor = GameDataProcessor()
    image_generator = Jinja2ImageGenerator()

    # Pick the first game to test with
    if schedule:
        game = schedule[0]
        print(f"🎮 Testing with first game: {game['away_name']} @ {game['home_name']}")
        print(f"   Game ID: {game['game_id']}")
        print()

        # Get boxscore
        print("📊 Fetching boxscore...")
        start_time = time.time()
        boxscore = mlb_client.get_boxscore(game['game_id'])
        boxscore_time = time.time() - start_time
        print(f"   ✅ Boxscore fetched in {boxscore_time:.2f}s")
        print()

        # Check if lineups are official
        lineups_official = mlb_client.are_lineups_official(boxscore)
        print(f"   Lineups Official: {lineups_official}")
        print()

        if lineups_official:
            home_team_id = game.get('home_id', 119)
            away_team_id = game.get('away_id', 119)

            print("⚾ Processing Away Team Lineup...")
            print(f"   Team: {game['away_name']} (ID: {away_team_id})")
            print("-" * 80)

            start_time = time.time()
            away_lineup = mlb_client.extract_lineup_data(boxscore, 'away', away_team_id)
            away_time = time.time() - start_time

            print(f"\n   ✅ Away lineup processed in {away_time:.2f}s")
            print(f"   Players processed: {len(away_lineup)}")
            print()

            # Show first 3 players as sample
            if away_lineup:
                print("   Sample players:")
                for player in away_lineup[:3]:
                    print(f"      {player['order']}. {player['name']} ({player['position']}) - {player['recent_stats']}")
            print()

            print("⚾ Processing Home Team Lineup...")
            print(f"   Team: {game['home_name']} (ID: {home_team_id})")
            print("-" * 80)

            start_time = time.time()
            home_lineup = mlb_client.extract_lineup_data(boxscore, 'home', home_team_id)
            home_time = time.time() - start_time

            print(f"\n   ✅ Home lineup processed in {home_time:.2f}s")
            print(f"   Players processed: {len(home_lineup)}")
            print()

            # Show first 3 players as sample
            if home_lineup:
                print("   Sample players:")
                for player in home_lineup[:3]:
                    print(f"      {player['order']}. {player['name']} ({player['position']}) - {player['recent_stats']}")
            print()

            # Process pitchers
            print("⚾ Processing Starting Pitchers...")
            print("-" * 80)

            away_pitchers = mlb_client.extract_pitcher_data(boxscore, 'away', away_team_id)
            home_pitchers = mlb_client.extract_pitcher_data(boxscore, 'home', home_team_id)

            if away_pitchers:
                print(f"   Away: {away_pitchers[0]['name']} - {away_pitchers[0]['recent_stats']}")
            if home_pitchers:
                print(f"   Home: {home_pitchers[0]['name']} - {home_pitchers[0]['recent_stats']}")
            print()

            # Generate lineup card image if requested
            if generate_images:
                print("🎨 Generating Lineup Card Image...")
                print("-" * 80)

                # Use game_processor to get full game data
                game_data = game_processor.get_game_data(game)

                # Create output directory
                images_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'images', 'test')
                os.makedirs(images_dir, exist_ok=True)

                # Create filename
                away_team_clean = game['away_name'].replace(' ', '_').replace('.', '')
                home_team_clean = game['home_name'].replace(' ', '_').replace('.', '')
                output_filename = f"test_lineup_{away_team_clean}_vs_{home_team_clean}_{game['game_id']}.png"
                output_path = os.path.join(images_dir, output_filename)

                # Format game data for image generator
                formatted_game_data = {
                    'away_team': game['away_name'],
                    'home_team': game['home_name'],
                    'game_date': game_data.get('game_date', date_str),
                    'game_time': game_data.get('game_time', 'TBD'),
                    'game_location': game_data.get('venue', 'Unknown Venue'),
                    'away_lineup': away_lineup,
                    'home_lineup': home_lineup,
                    'away_pitcher': {
                        'name': away_pitchers[0]['name'] if away_pitchers else 'TBD',
                        'position': 'P',
                        'stats': away_pitchers[0]['recent_stats'] if away_pitchers else 'No data'
                    },
                    'home_pitcher': {
                        'name': home_pitchers[0]['name'] if home_pitchers else 'TBD',
                        'position': 'P',
                        'stats': home_pitchers[0]['recent_stats'] if home_pitchers else 'No data'
                    }
                }

                try:
                    success = image_generator.create_lineup_image(formatted_game_data, output_path)
                    if success:
                        print(f"   ✅ Lineup card created: {output_filename}")
                        print(f"   📁 Saved to: {output_path}")
                    else:
                        print(f"   ❌ Failed to create lineup card")
                except Exception as e:
                    print(f"   ❌ Error creating lineup card: {e}")
                print()

            # Show cache statistics
            print("=" * 80)
            print("📊 API Cache Statistics (After Processing One Game)")
            print("=" * 80)
            cache_stats = cache.get_cache_stats()
            print(f"   Player IDs cached: {cache_stats['player_ids_cached']}")
            print(f"   Boxscores cached: {cache_stats['boxscores_cached']}")
            print(f"   Schedules cached: {cache_stats['schedules_cached']}")
            print()
            print(f"   Total players processed: {len(away_lineup) + len(home_lineup) + 2}")
            print(f"   Total processing time: {away_time + home_time:.2f}s")
            print()
            print("💡 Optimization Impact:")
            print(f"   - Only 2 schedule fetches (1 per team) instead of {len(away_lineup) + len(home_lineup) + 2}")
            print(f"   - Player IDs cached for future lookups")
            print(f"   - Boxscores cached and reused")
            print()

            # Calculate what the old system would have done
            old_api_calls = (len(away_lineup) + len(home_lineup) + 2) * 2  # 2 calls per player (lookup + schedule)
            old_api_calls += (len(away_lineup) + len(home_lineup)) * 10  # ~10 boxscore fetches per player
            new_api_calls = cache_stats['player_ids_cached'] + cache_stats['schedules_cached'] + cache_stats['boxscores_cached']

            reduction_pct = ((old_api_calls - new_api_calls) / old_api_calls) * 100 if old_api_calls > 0 else 0

            print(f"   Estimated OLD system: ~{old_api_calls} API calls")
            print(f"   NEW optimized system: ~{new_api_calls} API calls")
            print(f"   Reduction: ~{reduction_pct:.0f}%")
            print()

        else:
            print("⚠️  Lineups not official yet for this game")
            print("   This is expected for games before lineup announcements")

    print("=" * 80)
    print("Test Complete!")
    print("=" * 80)


if __name__ == "__main__":
    # Test with August 8th, 2025
    test_date = "2025-08-08"

    print()
    print("🚀 MLBMatchupXBot - Historical Date Test with Image Generation")
    print()
    print(f"Testing optimization + lineup card generation with real game data from {test_date}")
    print()

    test_historical_date(test_date, generate_images=True)
