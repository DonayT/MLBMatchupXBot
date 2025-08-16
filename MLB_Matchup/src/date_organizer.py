import os
import shutil
from datetime import datetime, timedelta
import json
from get_stats import initialize_stats_cache, clear_stats_cache

"""
params: None
returns: bool - True if date transition detected and reset performed, False otherwise
summary: Check if we've moved to a new date and need to reset processed games and stats cache
"""
def check_date_transition():
    today = datetime.now().strftime('%Y-%m-%d')
    last_processed_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'last_processed_date.txt')
    
    os.makedirs(os.path.dirname(last_processed_file), exist_ok=True)
    
    if os.path.exists(last_processed_file):
        with open(last_processed_file, 'r') as f:
            last_date = f.read().strip()
        
        if last_date != today:
            processed_games_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'processed_games.json')
            if os.path.exists(processed_games_file):
                with open(processed_games_file, 'w') as f:
                    json.dump([], f)
            
            print("New day detected - initializing fresh stats cache...")
            clear_stats_cache()  # Clear the old cache first
            initialize_stats_cache()  # Initialize fresh cache
            print("Stats cache initialized for new day!")
            
            with open(last_processed_file, 'w') as f:
                f.write(today)
            
            return True
    else:
        with open(last_processed_file, 'w') as f:
            f.write(today)
    
    return False

"""
params: None
returns: None
summary: Organize existing images into date-based folders based on filename patterns
"""
def organize_existing_images():
    base_images_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'images')
    
    os.makedirs(base_images_dir, exist_ok=True)
    
    loose_images = []
    for file in os.listdir(base_images_dir):
        if file.endswith('.png') and not os.path.isdir(os.path.join(base_images_dir, file)):
            loose_images.append(file)
    
    if loose_images:
        for image_file in loose_images:
            try:
                import re
                date_match = re.search(r'(\d{4}-\d{2}-\d{2})', image_file)
                if date_match:
                    date_folder = date_match.group(1)
                else:
                    date_folder = datetime.now().strftime('%Y-%m-%d')
                
                date_dir = os.path.join(base_images_dir, date_folder)
                os.makedirs(date_dir, exist_ok=True)
                
                old_path = os.path.join(base_images_dir, image_file)
                new_path = os.path.join(date_dir, image_file)
                
                if not os.path.exists(new_path):
                    shutil.move(old_path, new_path)
                    
            except Exception as e:
                pass 