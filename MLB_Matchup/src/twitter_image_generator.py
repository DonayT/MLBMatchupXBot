from PIL import Image, ImageDraw, ImageFont
import os

class TwitterImageGenerator:
    def __init__(self):
        # Twitter image dimensions (1200x675 is optimal for Twitter)
        self.width = 1200
        self.height = 675
        
        # Colors - Clean and simple
        self.background_color = (255, 255, 255)  # White
        self.text_color = (0, 0, 0)  # Black
        self.title_color = (0, 0, 0)  # Black for title
        self.divider_color = (200, 200, 200)  # Light gray for dividers
        
        # Fonts - Clean and readable
        try:
            self.title_font = ImageFont.truetype("arial.ttf", 32)
            self.header_font = ImageFont.truetype("arial.ttf", 20)
            self.body_font = ImageFont.truetype("arial.ttf", 16)
            self.pitcher_font = ImageFont.truetype("arial.ttf", 18)
        except:
            # Fallback to default font
            self.title_font = ImageFont.load_default()
            self.header_font = ImageFont.load_default()
            self.body_font = ImageFont.load_default()
            self.pitcher_font = ImageFont.load_default()
    
    def create_lineup_image(self, game_data, output_path):
        """Create a clean lineup image with side-by-side layout"""
        
        # Create the base image
        image = Image.new('RGB', (self.width, self.height), self.background_color)
        draw = ImageDraw.Draw(image)
        
        # Draw title at the top
        title = f"{game_data['away_team']} @ {game_data['home_team']}"
        title_bbox = draw.textbbox((0, 0), title, font=self.title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (self.width - title_width) // 2
        draw.text((title_x, 30), title, font=self.title_font, fill=self.title_color)
        
        # Draw pitchers section at the top
        pitcher_y = 90
        draw.text((50, pitcher_y), "Starting Pitchers", font=self.header_font, fill=self.text_color)
        
        # Away pitcher (left side)
        away_pitcher_text = f"{game_data['away_team']}: {game_data['away_pitcher']}"
        draw.text((50, pitcher_y + 30), away_pitcher_text, font=self.pitcher_font, fill=self.text_color)
        
        # Home pitcher (right side)
        home_pitcher_text = f"{game_data['home_team']}: {game_data['home_pitcher']}"
        home_pitcher_bbox = draw.textbbox((0, 0), home_pitcher_text, font=self.pitcher_font)
        home_pitcher_width = home_pitcher_bbox[2] - home_pitcher_bbox[0]
        home_pitcher_x = self.width - 50 - home_pitcher_width
        draw.text((home_pitcher_x, pitcher_y + 30), home_pitcher_text, font=self.pitcher_font, fill=self.text_color)
        
        # Draw divider line
        draw.line([(50, pitcher_y + 70), (self.width - 50, pitcher_y + 70)], 
                  fill=self.divider_color, width=1)
        
        # Draw lineups side by side
        lineup_y = pitcher_y + 100
        
        # Away team lineup (left side)
        draw.text((50, lineup_y), f"{game_data['away_team']} Lineup", font=self.header_font, fill=self.text_color)
        
        for i, player in enumerate(game_data['away_lineup']):
            player_text = f"{player['order']}. {player['name']} ({player['position']})"
            draw.text((50, lineup_y + 35 + (i * 25)), player_text, font=self.body_font, fill=self.text_color)
        
        # Home team lineup (right side)
        home_x = self.width // 2 + 50
        draw.text((home_x, lineup_y), f"{game_data['home_team']} Lineup", font=self.header_font, fill=self.text_color)
        
        for i, player in enumerate(game_data['home_lineup']):
            player_text = f"{player['order']}. {player['name']} ({player['position']})"
            draw.text((home_x, lineup_y + 35 + (i * 25)), player_text, font=self.body_font, fill=self.text_color)
        
        # Add timestamp at bottom
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        timestamp_text = f"Generated: {timestamp}"
        timestamp_bbox = draw.textbbox((0, 0), timestamp_text, font=self.body_font)
        timestamp_width = timestamp_bbox[2] - timestamp_bbox[0]
        timestamp_x = (self.width - timestamp_width) // 2
        draw.text((timestamp_x, self.height - 40), timestamp_text, font=self.body_font, fill=self.divider_color)
        
        # Save the image
        image.save(output_path)
        print(f"Twitter image saved: {output_path}")
        
        return output_path

# Example usage function
def create_twitter_image(game_data):
    """Create a Twitter image for the given game data"""
    generator = TwitterImageGenerator()
    
    # Create filename based on game info
    filename = f"lineup_{game_data['away_team'].replace(' ', '_')}_vs_{game_data['home_team'].replace(' ', '_')}_{game_data['game_id']}.png"
    
    # Get today's date for folder organization
    from datetime import datetime
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Create date-based folder structure
    base_images_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'images')
    date_folder = os.path.join(base_images_dir, today)
    os.makedirs(date_folder, exist_ok=True)
    
    # Save to date-specific folder
    output_path = os.path.join(date_folder, filename)
    
    print(f"📁 Saving to date folder: {today}")
    
    return generator.create_lineup_image(game_data, output_path) 