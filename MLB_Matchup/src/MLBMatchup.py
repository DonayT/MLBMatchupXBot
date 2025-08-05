import statsapi
from datetime import datetime
import pprint
from twitter_image_generator import create_twitter_image
import json
import os
import sys
import subprocess
import get_address

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
        # pprint.pprint(venue)  # Commented out for performance
        venue_name = venue.get('name', 'Unknown Venue')
        # print(venue_name)  # Commented out for performance
        
        # Get city and state from venue name
        if venue_name != 'Unknown Venue':
            try:
                city_state = get_address.get_city_state(venue_name)
                if city_state:
                    city, state = city_state.split(', ')
                else:
                    city = 'Unknown City'
                    state = 'Unknown State'
            except Exception as e:
                print(f"   Error getting city/state for {venue_name}: {e}")
                city = 'Unknown City'
                state = 'Unknown State'
        else:
            city = 'Unknown City'
            state = 'Unknown State'

    # print(game.keys())  # Commented out for performance
    
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

def upload_image_to_twitter(image_path, game_data):
    """Upload the generated image to Twitter using bot.py"""
    try:
        with open("MLB_Matchup/config/teamHashtags.json", "r") as f:
            teamHashtags = json.load(f)
        # Create tweet text with game information in the desired format
        away_hashtag = teamHashtags.get(game_data['away_team'], f"#{game_data['away_team'].replace(' ', '')}")
        home_hashtag = teamHashtags.get(game_data['home_team'], f"#{game_data['home_team'].replace(' ', '')}")

        with open("MLB_Matchup/config/teamAbreviations.json", "r") as f:
            teamAbreviations = json.load(f)
        away_abr = teamAbreviations.get(game_data['away_team'], game_data['away_team'][:3].upper())
        home_abr = teamAbreviations.get(game_data['home_team'], game_data['home_team'][:3].upper())
        
        tweet_text = f"{game_data['away_team']} @ {game_data['home_team']}\n"
        tweet_text += f"🕐 {game_data['game_time']} 📅 {game_data['game_date']}\n"
        tweet_text += f"{away_hashtag} {home_hashtag}\n"
        tweet_text += f"#{away_abr}vs{home_abr} // #{home_abr}vs{away_abr}"
        
        # Call bot.py with the image path and tweet text
        # We'll need to modify bot.py to accept command line arguments
        cmd = [
            "python", 
            "Xbot/bot.py",
            "--image", image_path,
            "--text", tweet_text
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"   Successfully uploaded image to Twitter")
        else:
            print(f"   Error uploading to Twitter: {result.stderr}")
            
    except Exception as e:
        print(f"   Error calling bot.py: {e}")

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

                # Upload image to Twitter
                upload_image_to_twitter(image_path, game_data)
                
            except Exception as e:
                print(f"   Error creating image: {e}")
        else:
            print("   Waiting for lineups to become official...")
        
        print()
    
    return "CONTINUE"

if __name__ == "__main__":
    result = process_games()
    if result == "ALL_DONE":
        print("✅ All games processed successfully - exiting cleanly")
        exit(0)  # Success exit code for "all done"
    else:
        exit(0)   # Normal exit
