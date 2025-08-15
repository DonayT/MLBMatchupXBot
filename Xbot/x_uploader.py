import json
import subprocess
import os 

def upload_image_to_twitter(image_path, game_data):
    """Upload the generated image to Twitter using bot.py"""
    try:
        # Get the current directory (Xbot) and navigate to config files
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_dir = os.path.join(current_dir, '..', 'MLB_Matchup', 'config')
        
        with open(os.path.join(config_dir, "teamHashtags.json"), "r") as f:
            teamHashtags = json.load(f)
        # Create tweet text with game information in the desired format
        away_hashtag = teamHashtags.get(game_data['away_team'], f"#{game_data['away_team'].replace(' ', '')}")
        home_hashtag = teamHashtags.get(game_data['home_team'], f"#{game_data['home_team'].replace(' ', '')}")

        with open(os.path.join(config_dir, "teamAbreviations.json"), "r") as f:
            teamAbreviations = json.load(f)
        away_abr = teamAbreviations.get(game_data['away_team'], game_data['away_team'][:3].upper())
        home_abr = teamAbreviations.get(game_data['home_team'], game_data['home_team'][:3].upper())
        
        tweet_text = f"{game_data['away_team']} @ {game_data['home_team']}\n"
        tweet_text += f"🕐 {game_data['game_time']} 📅 {game_data['game_date']}\n"
        tweet_text += f"*Batter statistics are over last 5 games*\n*Pitcher statistics are over last 3 outtings*\n"
        tweet_text += f"{away_hashtag} {home_hashtag}\n"
        tweet_text += f"#{away_abr}vs{home_abr} // #{home_abr}vs{away_abr}"
        
        # Call bot.py with the image path and tweet text
        # bot.py is in the same directory as this file
        bot_path = os.path.join(current_dir, "bot.py")
        cmd = [
            "python", 
            bot_path,
            "--image", image_path,
            "--text", tweet_text
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            # Keep error logging for debugging
            pass
            
    except Exception as e:
        # Keep error logging for debugging
        pass