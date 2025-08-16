import json
import os
from datetime import datetime

class GameQueue:
    def __init__(self, queue_file=None):
        if queue_file is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            queue_file = os.path.join(script_dir, "..", "data", "processed_games.json")
        self.queue_file = queue_file
        self.processed_games = self.load_processed_games()

    """
    params: None
    returns: list - List of processed game IDs loaded from the queue file
    summary: Load the list of already processed games from the JSON file
    """
    def load_processed_games(self):
        if os.path.exists(self.queue_file):
            try:
                with open(self.queue_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading processed games: {e}")
                return []
        return []
    
    """
    params: None
    returns: None
    summary: Save the current list of processed games to the JSON file
    """
    def save_processed_games(self):
        try:
            os.makedirs(os.path.dirname(self.queue_file), exist_ok=True)
            with open(self.queue_file, 'w') as f:
                json.dump(self.processed_games, f)
        except Exception as e:
            print(f"Error saving processed games: {e}")

    """
    params: game_id (int) - MLB game ID to check
    returns: bool - True if game has been processed, False otherwise
    summary: Check if a specific game has already been processed
    """
    def is_processed(self, game_id):
        return game_id in self.processed_games

    """
    params: game_id (int) - MLB game ID to mark as processed
    returns: None
    summary: Mark a game as processed and save to the queue file
    """
    def mark_processed(self, game_id):
        if game_id not in self.processed_games:
            self.processed_games.append(game_id)
            self.save_processed_games()

    """
    params: schedule (list) - List of game dictionaries from MLB schedule
    returns: list - List of games that haven't been processed yet
    summary: Filter schedule to return only unprocessed games
    """
    def get_unprocessed_games(self, schedule):
        unprocessed = []
        for game in schedule:
            if not self.is_processed(game['game_id']):
                unprocessed.append(game)
        return unprocessed

    """
    params: None
    returns: int - Number of games that have been processed
    summary: Get the count of processed games
    """
    def get_processed_count(self):
        return len(self.processed_games)

    """
    params: None
    returns: None
    summary: Clear all processed games and reset the queue
    """
    def clear_processed_games(self):
        self.processed_games = []
        self.save_processed_games()

    """
    params: None
    returns: list - Copy of the processed games list
    summary: Get a copy of the current processed games list
    """
    def get_processed_games(self):
        return self.processed_games.copy()
