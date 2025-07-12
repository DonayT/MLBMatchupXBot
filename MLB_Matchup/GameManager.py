import statsapi
from Game import Game 
from GameQueue import GameQueue 

class GameManager: 
    def __init__(self, date):
        self.date = date
        self.game_queue = GameQueue()

    def load_games(self):
        schedule = statsapi.schedule(date = self.date)

        for game in schedule:
            g = Game(game_id = game['game_id'], date = self.date)

            try: 
                g.grab_boxscore()
                self.game_queue.enqueue(g)
            except Exception as e:
                print(f"Failed to fetch game {g.game_id}: {e}")

    def process_games(self):

        while not self.game_queue.is_empty():
            
            game = self.game_queue.deque()
            print(f"Processing {game.away_team} @ ()")

            for side in ['away', 'home']:
                print(f"{side.title()} Lineup:")
                for player in game.lineups[side]:
                    print(f"   {player['batting_order']}: {player['name']} - {player['position']}")
            print("-" * 40) 

