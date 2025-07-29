import os
import shutil
from datetime import datetime
import json

def organize_existing_images():
    """Move existing images to date-based folders"""
    base_images_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'images')
    
    if not os.path.exists(base_images_dir):
        print("❌ Images directory not found")
        return
    
    # Get all PNG files in the images directory
    png_files = [f for f in os.listdir(base_images_dir) if f.endswith('.png')]
    
    if not png_files:
        print("✅ No existing images to organize")
        return
    
    print(f"📁 Organizing {len(png_files)} existing images...")
    
    for filename in png_files:
        # Extract date from filename or use today's date as fallback
        # Format: lineup_Team1_vs_Team2_GameID.png
        try:
            # Try to extract date from the game ID or use file modification time
            file_path = os.path.join(base_images_dir, filename)
            mod_time = os.path.getmtime(file_path)
            file_date = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d')
            
            # Create date folder
            date_folder = os.path.join(base_images_dir, file_date)
            os.makedirs(date_folder, exist_ok=True)
            
            # Move file to date folder
            new_path = os.path.join(date_folder, filename)
            shutil.move(file_path, new_path)
            print(f"  📂 Moved {filename} to {file_date}/")
            
        except Exception as e:
            print(f"  ❌ Error moving {filename}: {e}")
    
    print("✅ Image organization complete!")

def check_date_transition():
    """Check if we need to reset processed games for a new day"""
    today = datetime.now().strftime('%Y-%m-%d')
    processed_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'processed_games.json')
    
    # Check if we have a last_processed_date file
    last_date_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'last_processed_date.txt')
    
    if os.path.exists(last_date_file):
        with open(last_date_file, 'r') as f:
            last_date = f.read().strip()
        
        if last_date != today:
            print(f"📅 Date changed from {last_date} to {today}")
            print("🔄 Resetting processed games for new day...")
            
            # Reset processed games for new day
            with open(processed_file, 'w') as f:
                json.dump([], f)
            
            # Update last processed date
            with open(last_date_file, 'w') as f:
                f.write(today)
            
            print("✅ Processed games reset for new day")
            return True
    else:
        # First time running, create the file
        with open(last_date_file, 'w') as f:
            f.write(today)
        print(f"📅 First run - setting date to {today}")
    
    return False

if __name__ == "__main__":
    print("🔄 MLB Lineup Bot - Date Organizer")
    print("=" * 40)
    
    # Check for date transition
    date_changed = check_date_transition()
    
    # Organize existing images
    organize_existing_images()
    
    if date_changed:
        print("\n🎯 Ready for new day!")
    else:
        print("\n✅ Date organization complete!") 