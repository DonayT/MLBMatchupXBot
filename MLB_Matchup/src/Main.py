from datetime import datetime
import statsapi

from game_data_processor import GameDataProcessor
from game_queue import GameQueue
from date_organizer import check_date_transition, organize_existing_images
from twitter_image_generator import create_twitter_image
from x_uploader import upload_image_to_twitter

class Main:
    def __init__(self):
        self.game_data_processor = GameDataProcessor()
        self.game_queue = GameQueue()

    def process_games(self):
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Check for date transition and organize images
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
        
        # Check if all games are processed
        if len(unprocessed_games) == 0:
            print("All games for today have been processed!")
            print("No more games to check - all lineups are complete!")
            return "ALL_DONE"
        
        for game in unprocessed_games:
            game_data = self.game_data_processor.get_game_data(game)
            
            print(f" {game_data['away_team']} @ {game_data['home_team']} - Game ID: {game_data['game_id']}")
            print(f"   Lineups Official: {game_data['lineups_official']}")
            
            if game_data['lineups_official']:
                
                try:
                    image_path = create_twitter_image(game_data)
                    
                    self.game_queue.mark_processed(game_data['game_id'])
                    print(f"   Game {game_data['game_id']} marked as processed")

                    upload_image_to_twitter(image_path, game_data)
                    
                except Exception as e:
                    print(f"   Error creating image: {e}")
            else:
                print("   Waiting for lineups to become official...")
            
            print()
    
        return "CONTINUE"
        