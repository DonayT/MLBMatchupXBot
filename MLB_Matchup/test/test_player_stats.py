"""
Test script for player game history functionality
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from MLB_API_Client import MLBAPIClient

def test_player_game_history():
    # Initialize the API client
    client = MLBAPIClient()
    # Test with a well-known player
    test_players = ['Juan Soto', 'Roman Anthony', 'Pete Crow-Armstrong']
    for player in test_players:
        print(f"\nPerformance summary for {player}:")
        summary = client.get_player_15_games_string(player)
        print(summary)

if __name__ == "__main__":
    test_player_game_history()