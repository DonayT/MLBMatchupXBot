import os
import shutil
from datetime import datetime, timedelta
import json

def check_date_transition():
    """Check if we've moved to a new date and need to reset processed games"""
    today = datetime.now().strftime('%Y-%m-%d')
    last_processed_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'last_processed_date.txt')
    
    # Create data directory if it doesn't exist
    os.makedirs(os.path.dirname(last_processed_file), exist_ok=True)
    
    # Check if we have a last processed date
    if os.path.exists(last_processed_file):
        with open(last_processed_file, 'r') as f:
            last_date = f.read().strip()
        
        # If it's a new date, we need to reset
        if last_date != today:
            print(f"Date changed from {last_date} to {today}")
            print("Resetting processed games for new day...")
            
            # Clear processed games for new day
            processed_games_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'processed_games.json')
            if os.path.exists(processed_games_file):
                with open(processed_games_file, 'w') as f:
                    json.dump([], f)
                print("Cleared processed games list")
            
            # Update last processed date
            with open(last_processed_file, 'w') as f:
                f.write(today)
            
            return True
    else:
        # First time running, create the file
        with open(last_processed_file, 'w') as f:
            f.write(today)
        print(f"First run - setting date to {today}")
    
    return False

def organize_existing_images():
    """Organize existing images into date-based folders"""
    base_images_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'images')
    
    # Create images directory if it doesn't exist
    os.makedirs(base_images_dir, exist_ok=True)
    
    # Check if there are any loose images in the base directory
    loose_images = []
    for file in os.listdir(base_images_dir):
        if file.endswith('.png') and not os.path.isdir(os.path.join(base_images_dir, file)):
            loose_images.append(file)
    
    if loose_images:
        print(f"Found {len(loose_images)} loose images to organize...")
        
        for image_file in loose_images:
            # Try to extract date from filename or use today's date
            try:
                # Look for date pattern in filename (e.g., 2025-07-30)
                import re
                date_match = re.search(r'(\d{4}-\d{2}-\d{2})', image_file)
                if date_match:
                    date_folder = date_match.group(1)
                else:
                    # Use today's date if no date found in filename
                    date_folder = datetime.now().strftime('%Y-%m-%d')
                
                # Create date folder
                date_dir = os.path.join(base_images_dir, date_folder)
                os.makedirs(date_dir, exist_ok=True)
                
                # Move the image
                old_path = os.path.join(base_images_dir, image_file)
                new_path = os.path.join(date_dir, image_file)
                
                if not os.path.exists(new_path):  # Don't overwrite
                    shutil.move(old_path, new_path)
                    print(f"  Moved {image_file} to {date_folder}/")
                else:
                    print(f"  {image_file} already exists in {date_folder}/")
                    
            except Exception as e:
                print(f"  Error organizing {image_file}: {e}")
        
        print("Image organization complete!")
    else:
        print("No loose images to organize") 