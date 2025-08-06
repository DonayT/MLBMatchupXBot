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
        
        date_changed = check_date_transition()
        organize_existing_images()
        
        schedule = statsapi.schedule(start_date=today, end_date=today)
        
        unprocessed_games = self.game_queue.get_unprocessed_games(schedule)
        
        if len(unprocessed_games) == 0:
            return "ALL_DONE"
        
        for game in unprocessed_games:
            game_data = self.game_data_processor.get_game_data(game)
            
            if game_data['lineups_official']:
                try:
                    image_path = create_twitter_image(game_data)
                    
                    self.game_queue.mark_processed(game_data['game_id'])

                    upload_image_to_twitter(image_path, game_data)
                    
                except Exception as e:
                    print(f"   Error creating image: {e}")
            else:
                pass
    
        return "CONTINUE"
        