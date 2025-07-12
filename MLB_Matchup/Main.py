from datetime import datetime
from GameManager import GameManager

if __name__ == "__main__":
    today = datetime.today().strftime("%m/%d/%Y") 
    manager = GameManager(today)
    manager.load_games()
    manager.process_games()