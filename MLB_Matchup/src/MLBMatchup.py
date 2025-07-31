import statsapi
from datetime import datetime
import pprint
from twitter_image_generator import create_twitter_image
import json
import os
import sys

# Add src directory to path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import date organizer
from date_organizer import check_date_transition, organize_existing_images

class GameQueue:
    def __init__(self, queue_file=None):
        if queue_file is None:
            # Get the directory where this script is located
            script_dir = os.path.dirname(os.path.abspath(__file__))
            # Go up one level to the MLB_Matchup directory, then to data
            queue_file = os.path.join(script_dir, "..", "data", "processed_games.json")
        self.queue_file = queue_file
        self.processed_games = self.load_processed_games()
    
    def load_processed_games(self):
        """Load previously processed games from file"""
        if os.path.exists(self.queue_file):
            try:
                with open(self.queue_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_processed_games(self):
        """Save processed games to file"""
        with open(self.queue_file, 'w') as f:
            json.dump(self.processed_games, f)
    
    def is_processed(self, game_id):
        """Check if a game has already been processed"""
        return game_id in self.processed_games
    
    def mark_processed(self, game_id):
        """Mark a game as processed"""
        if game_id not in self.processed_games:
            self.processed_games.append(game_id)
            self.save_processed_games()
    
    def get_unprocessed_games(self, schedule):
        """Get games that haven't been processed yet"""
        unprocessed = []
        for game in schedule:
            if not self.is_processed(game['game_id']):
                unprocessed.append(game)
        return unprocessed

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
    
    game_data = {
        'game_id': game_id,
        'home_team': home,
        'away_team': away,
        'home_pitcher': home_pitcher,
        'away_pitcher': away_pitcher,
        'home_lineup': [],
        'away_lineup': [],
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

def process_games():
    """Main function to process games with queue system"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Check for date transition and organize images
    print("Checking date organization...")
    date_changed = check_date_transition()
    organize_existing_images()
    print()
    
    # Initialize queue
    game_queue = GameQueue()
    
    # Get today's schedule
    schedule = statsapi.schedule(start_date=today, end_date=today)
    
    # Get only unprocessed games
    unprocessed_games = game_queue.get_unprocessed_games(schedule)
    
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
        game_data = get_game_data(game)
        
        print(f" {game_data['away_team']} @ {game_data['home_team']} - Game ID: {game_data['game_id']}")
        print(f"   Home SP: {game_data['home_pitcher']}")
        print(f"   Away SP: {game_data['away_pitcher']}")
        print(f"   Lineups Official: {game_data['lineups_official']}")
        
        if game_data['lineups_official']:
            print("  Both lineups are official - generating image!")
            
            # Generate Twitter image
            try:
                image_path = create_twitter_image(game_data)
                print(f"   Twitter image created: {image_path}")
                
                # Mark as processed
                game_queue.mark_processed(game_data['game_id'])
                print(f"   Game {game_data['game_id']} marked as processed")
                
            except Exception as e:
                print(f"   Error creating image: {e}")
        else:
            print("   Waiting for lineups to become official...")
        
        print()
    
    return "CONTINUE"

if __name__ == "__main__":
    result = process_games()
    if result == "ALL_DONE":
        exit(42)  # Special exit code for "all done"
    else:
        exit(0)   # Normal exit
