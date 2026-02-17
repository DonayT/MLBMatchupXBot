from datetime import datetime
import statsapi
import os
import sys

# Add utils and image_generation directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'utils'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'image_generation'))

from game_data_processor import GameDataProcessor
from game_queue import GameQueue
from date_organizer import check_date_transition, organize_existing_images
from jinja2_image_generator import Jinja2ImageGenerator
from get_stats import clear_stats_cache
from api_cache import get_cache

# Add Xbot directory to path for x_uploader import
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Xbot'))
from x_uploader import upload_image_to_twitter

class MLBMatchup:
    def __init__(self):
        self.game_data_processor = GameDataProcessor()
        self.game_queue = GameQueue()
        self.jinja2_generator = Jinja2ImageGenerator()

    """
    params: None
    returns: str - "ALL_DONE" if all games processed, "CONTINUE" if more games remain
    summary: Main workflow that processes MLB games, creates lineup images, and uploads to Twitter
    """
    def process_games(self):
        today = datetime.now().strftime('%Y-%m-%d')
        
        print("Checking date organization...")
        date_changed = check_date_transition()
        organize_existing_images()
        print()
        
        schedule = statsapi.schedule(start_date=today, end_date=today)
        
        unprocessed_games = self.game_queue.get_unprocessed_games(schedule)
        
        print(f"Processing {len(unprocessed_games)} unprocessed games for {today}")
        print(f"Total games today: {len(schedule)}")
        print(f"Already processed: {len(schedule) - len(unprocessed_games)}")
        print()
        
        if len(unprocessed_games) == 0:
            print("All games for today have been processed!")
            print("No more games to check - all lineups are complete!")

            print("Clearing stats cache for fresh data tomorrow...")
            clear_stats_cache()
            print("Stats cache cleared successfully!")

            print("Clearing API cache for fresh data tomorrow...")
            cache = get_cache()
            cache.clear()
            print("API cache cleared successfully!")

            return "ALL_DONE"
        
        for game in unprocessed_games:
            game_data = self.game_data_processor.get_game_data(game)
            
            print(f" {game_data['away_team']} @ {game_data['home_team']} - Game ID: {game_data['game_id']}")
            print(f"   Lineups Official: {game_data['lineups_official']}")
            
            if game_data['lineups_official']:
                
                try:
                    # Create image using the new Jinja2 system
                    image_path = self.create_lineup_image_with_jinja2(game_data)
                    
                    self.game_queue.mark_processed(game_data['game_id'])
                    print(f"   Game {game_data['game_id']} marked as processed")

                    upload_image_to_twitter(image_path, game_data)
                    
                except Exception as e:
                    print(f"   Error creating image: {e}")
            else:
                print("   Waiting for lineups to become official...")

            print()

        # Show cache statistics to demonstrate optimization effectiveness
        cache = get_cache()
        cache_stats = cache.get_cache_stats()
        print("\n📊 API Cache Statistics:")
        print(f"   Player IDs cached: {cache_stats['player_ids_cached']}")
        print(f"   Boxscores cached: {cache_stats['boxscores_cached']}")
        print(f"   Schedules cached: {cache_stats['schedules_cached']}")
        print(f"   💡 Optimization: Avoided {cache_stats['player_ids_cached']} player lookups, {cache_stats['schedules_cached']} schedule fetches!\n")

        return "CONTINUE"
    
    def create_lineup_image_with_jinja2(self, game_data):
        """Create lineup image using the new Jinja2 system"""
        try:
            # Prepare the output path in the images folder with date organization
            images_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'images')
            
            # Create date folder (YYYY-MM-DD format)
            game_date = game_data['game_date']
            if game_date and game_date != 'Unknown':
                # Convert MM/DD/YYYY to YYYY-MM-DD format
                try:
                    from datetime import datetime
                    parsed_date = datetime.strptime(game_date, '%m/%d/%Y')
                    date_folder = parsed_date.strftime('%Y-%m-%d')
                except:
                    # Fallback to today's date if parsing fails
                    from datetime import datetime
                    date_folder = datetime.now().strftime('%Y-%m-%d')
            else:
                # Use today's date if no game date available
                from datetime import datetime
                date_folder = datetime.now().strftime('%Y-%m-%d')
            
            # Create the full path with date folder
            date_images_dir = os.path.join(images_dir, date_folder)
            os.makedirs(date_images_dir, exist_ok=True)
            
            # Create filename based on game info
            away_team_clean = game_data['away_team'].replace(' ', '_').replace('.', '')
            home_team_clean = game_data['home_team'].replace(' ', '_').replace('.', '')
            game_id = game_data['game_id']
            
            output_filename = f"lineup_{away_team_clean}_vs_{home_team_clean}_{game_id}.png"
            output_path = os.path.join(date_images_dir, output_filename)
            
            print(f"   🎨 Creating Jinja2 lineup image...")
            print(f"   📁 Saving to: images/{date_folder}/")
            
            # Debug: Print the structure of the lineup data
            print(f"   🔍 Debug - Away lineup structure:")
            if game_data['away_lineup']:
                print(f"      First player: {game_data['away_lineup'][0]}")
            print(f"   🔍 Debug - Home lineup structure:")
            if game_data['home_lineup']:
                print(f"      First player: {game_data['home_lineup'][0]}")
            
            # Format the game data to match what Jinja2ImageGenerator expects
            # Fix: Map the lineup data correctly with stats field and preserve OPS trend
            formatted_away_lineup = []
            for player in game_data['away_lineup']:
                formatted_away_lineup.append({
                    'name': player.get('name', 'TBD'),
                    'position': player.get('position', ''),
                    'stats': player.get('recent_stats', 'No recent data'),  # Map recent_stats to stats
                    'ops_trend': player.get('ops_trend', 'neutral')  # Preserve OPS trend for color coding
                })
            
            formatted_home_lineup = []
            for player in game_data['home_lineup']:
                formatted_home_lineup.append({
                    'name': player.get('name', 'TBD'),
                    'position': player.get('position', ''),
                    'stats': player.get('recent_stats', 'No recent data'),  # Map recent_stats to stats
                    'ops_trend': player.get('ops_trend', 'neutral')  # Preserve OPS trend for color coding
                })
            
            formatted_game_data = {
                'away_team': game_data['away_team'],
                'home_team': game_data['home_team'],
                'game_date': game_data['game_date'],
                'game_time': game_data['game_time'],
                'game_location': game_data['venue'],  # Just show stadium name
                'away_lineup': formatted_away_lineup,
                'home_lineup': formatted_home_lineup,
                'away_pitcher': {
                    'name': game_data['away_pitcher'] if game_data['away_pitcher'] != 'TBD' else 'TBD',
                    'position': 'P',
                    'stats': game_data['away_pitchers'][0].get('recent_stats', 'No recent data') if game_data['away_pitchers'] else 'No recent data'
                },
                'home_pitcher': {
                    'name': game_data['home_pitcher'] if game_data['home_pitcher'] != 'TBD' else 'TBD',
                    'position': 'P',
                    'stats': game_data['home_pitchers'][0].get('recent_stats', 'No recent data') if game_data['home_pitchers'] else 'No recent data'
                }
            }
            
            # Use the new Jinja2ImageGenerator to create the image
            success = self.jinja2_generator.create_lineup_image(formatted_game_data, output_path)
            
            if success:
                print(f"   ✅ Jinja2 lineup image created: {output_filename}")
                return output_path
            else:
                raise Exception("Failed to create image with Jinja2ImageGenerator")
                
        except Exception as e:
            print(f"   ❌ Error in Jinja2 image creation: {e}")
            raise e