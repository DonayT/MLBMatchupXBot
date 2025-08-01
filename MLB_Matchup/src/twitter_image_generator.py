from PIL import Image, ImageDraw, ImageFont
import os
import json

class TwitterImageGenerator:
    def __init__(self):
        # Image dimensions for the new layout
        self.width = 800
        self.height = 1000
        
        # Colors
        self.background_color = (255, 255, 255)  # White
        self.text_color = (0, 0, 0)  # Black
        self.divider_color = (200, 200, 200)  # Light gray
        
        # Load team colors
        self.team_colors = self.load_team_colors()
        self.team_secondary_colors = self.load_team_secondary_colors()
        
        # Fonts
        try:
            self.font_big = ImageFont.truetype("arialbd.ttf", 140)
            self.font_vs = ImageFont.truetype("arialbd.ttf", 60)
            self.font_mid = ImageFont.truetype("arialbd.ttf", 32)
            self.font_bold = ImageFont.truetype("arialbd.ttf", 36)
            self.font_reg = ImageFont.truetype("arial.ttf", 32)
        except:
            # Fallback to default font
            self.font_big = ImageFont.load_default()
            self.font_vs = ImageFont.load_default()
            self.font_mid = ImageFont.load_default()
            self.font_bold = ImageFont.load_default()
            self.font_reg = ImageFont.load_default()
    
    def load_team_colors(self):
        """Load team colors from JSON file"""
        try:
            config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'teamPrimaryColors.json')
            with open(config_path, "r") as f:
                return json.load(f)
        except:
            return {}
    
    def load_team_secondary_colors(self):
        """Load team secondary colors from JSON file"""
        try:
            config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'teamSecondaryColors.json')
            with open(config_path, "r") as f:
                return json.load(f)
        except:
            return {}
    
    def load_team_abbreviations(self):
        """Load team abbreviations from JSON file"""
        try:
            config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'teamAbreviations.json')
            with open(config_path, "r") as f:
                return json.load(f)
        except:
            return {}
    
    def create_lineup_image(self, game_data, output_path):
        """Create a lineup image similar to the reference design"""
        
        # Create the base image
        image = Image.new('RGB', (self.width, self.height), self.background_color)
        draw = ImageDraw.Draw(image)
        
        # Get team abbreviations and colors
        team_abbreviations = self.load_team_abbreviations()
        away_abr = team_abbreviations.get(game_data['away_team'], game_data['away_team'][:3].upper())
        home_abr = team_abbreviations.get(game_data['home_team'], game_data['home_team'][:3].upper())
        away_color = self.team_colors.get(game_data['away_team'])
        home_color = self.team_colors.get(game_data['home_team'])
        
        # Draw team abbreviations at top with outlines - positioned like reference image
        # Away team abbreviation with outline
        outline_width = 5
        # Draw outline by drawing text multiple times with offsets
        away_secondary_color = self.team_secondary_colors.get(game_data['away_team'], "black")
        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx != 0 or dy != 0:  # Skip the center position
                    draw.text((80 + dx, 50 + dy), away_abr, font=self.font_big, fill=away_secondary_color)
        # Draw the main text
        draw.text((80, 50), away_abr, font=self.font_big, fill=away_color)
        
        # Home team abbreviation with outline
        home_secondary_color = self.team_secondary_colors.get(game_data['home_team'], "black")
        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx != 0 or dy != 0:  # Skip the center position
                    draw.text((self.width-280 + dx, 50 + dy), home_abr, font=self.font_big, fill=home_secondary_color)
        # Draw the main text
        draw.text((self.width-280, 50), home_abr, font=self.font_big, fill=home_color)
        
        # Draw VS centered between team abbreviations
        draw.text((self.width//2-40, 120), "VS", font=self.font_vs, fill=self.text_color)
        
        # Game date and venue info - centered below VS
        game_date = game_data.get('game_date', 'TBD')
        venue = game_data.get('venue', 'TBD')
        location = game_data.get('location', 'TBD')
        
        draw.text((self.width//2-80, 200), game_date, font=self.font_mid, fill=self.text_color)
        draw.text((self.width//2-80, 240), venue, font=self.font_mid, fill=self.text_color)
        draw.text((self.width//2-80, 280), location, font=self.font_mid, fill=self.text_color)
        
        # Draw table headers - positioned like reference image
        table_top = 340
        row_h = 60
        col_w = self.width//3
        
        # Header row
        draw.rectangle([0, table_top, self.width, table_top+row_h], fill="#e0e0e0")
        draw.line([(col_w, table_top), (col_w, self.height)], fill="black", width=2)
        draw.line([(2*col_w, table_top), (2*col_w, self.height)], fill="black", width=2)
        
        # Starting pitchers row
        draw.text((col_w//2-30, table_top+10), "SP", font=self.font_bold, fill="black")
        draw.text((col_w+col_w//2-30, table_top+10), "SP", font=self.font_bold, fill="black")
        draw.text((col_w//2+col_w, table_top+10), "SP", font=self.font_bold, fill="black")
        
        # Pitcher names
        away_sp = game_data.get('away_pitcher', 'TBD')
        home_sp = game_data.get('home_pitcher', 'TBD')
        draw.text((col_w//2-30, table_top+row_h+10), away_sp, font=self.font_bold, fill="black")
        draw.text((col_w+col_w//2-30, table_top+row_h+10), home_sp, font=self.font_bold, fill="black")
        
        # Draw lineups
        away_lineup = game_data.get('away_lineup', [])
        home_lineup = game_data.get('home_lineup', [])
        
        for i in range(9):
            y = table_top + row_h*(i+2)
            
            # Away team lineup (left column)
            draw.rectangle([0, y, col_w, y+row_h], fill="#f5f5f5" if i%2==0 else "white")
            if i < len(away_lineup):
                player = away_lineup[i]
                pos = player.get('position', '')
                name = player.get('name', '')
                draw.text((20, y+15), pos, font=self.font_reg, fill="black")
                draw.text((80, y+15), name, font=self.font_bold, fill="black")
            
            # Home team lineup (right column)
            draw.rectangle([col_w*2, y, self.width, y+row_h], fill="#f5f5f5" if i%2==0 else "white")
            if i < len(home_lineup):
                player = home_lineup[i]
                pos = player.get('position', '')
                name = player.get('name', '')
                draw.text((col_w*2+20, y+15), pos, font=self.font_reg, fill="black")
                draw.text((col_w*2+80, y+15), name, font=self.font_bold, fill="black")
        
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