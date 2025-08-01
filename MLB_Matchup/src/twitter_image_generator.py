from tkinter import X
from turtle import home
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
        
        # Fonts - load from config folder
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config')
        print(f"Looking for fonts in: {config_path}")
        
        try:
            # Load fonts from config folder
            anton_path = os.path.join(config_path, "anton.ttf")
            worksans_regular_path = os.path.join(config_path, "WorkSans-Regular.ttf")
            worksans_bold_path = os.path.join(config_path, "WorkSans-Bold.ttf")
            
            print(f"Checking if font files exist:")
            print(f"  Anton.ttf: {os.path.exists(anton_path)}")
            print(f"  WorkSans-Regular.ttf: {os.path.exists(worksans_regular_path)}")
            print(f"  WorkSans-Bold.ttf: {os.path.exists(worksans_bold_path)}")
            
            self.font_big = ImageFont.truetype(anton_path, 182)  # Team abbreviations
            self.font_vs = ImageFont.truetype(anton_path, 60)    # VS text
            self.font_mid = ImageFont.truetype(worksans_regular_path, 22)  # Time, stadium, location
            self.font_bold = ImageFont.truetype(worksans_bold_path, 30)  # Player names
            self.font_reg = ImageFont.truetype(worksans_regular_path, 30)  # Positions
            print("Successfully loaded custom fonts!")
        except Exception as e:
            print(f"Failed to load custom fonts: {e}")
            try:
                # Fallback to common system fonts
                self.font_big = ImageFont.truetype("arialbd.ttf", 182)  # Bold Arial for abbreviations
                self.font_vs = ImageFont.truetype("arialbd.ttf", 60)    # Bold Arial for VS
                self.font_mid = ImageFont.truetype("arial.ttf", 22)     # Regular Arial for info
                self.font_bold = ImageFont.truetype("arialbd.ttf", 33)  # Bold Arial for names
                self.font_reg = ImageFont.truetype("arial.ttf", 33)     # Regular Arial for positions
                print("Using Arial fonts as fallback")
            except Exception as e2:
                print(f"Failed to load Arial fonts: {e2}")
                # Final fallback to default font
                self.font_big = ImageFont.load_default()
                self.font_vs = ImageFont.load_default()
                self.font_mid = ImageFont.load_default()
                self.font_bold = ImageFont.load_default()
                self.font_reg = ImageFont.load_default()
                print("Using system default fonts")
    
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

    def get_centered_text_xy(self, draw, text, font, center):
        
        cx, cy = center
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = cx - text_width // 2
        y = cy - text_height // 2

        return x, y

    
    def create_lineup_image(self, game_data, output_path):
        """Create a lineup image using a template image with text overlay"""
        
        # Load the template image
        try:
            template_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates', 'lineupTemplate.png')
            image = Image.open(template_path).convert('RGB')
            # Resize template to match our dimensions if needed
            image = image.resize((self.width, self.height))
        except:
            # Fallback to creating a blank image if template not found
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
        x, y = self.get_centered_text_xy(draw, away_abr, self.font_big, (160, 40))
        away_secondary_color = self.team_secondary_colors.get(game_data['away_team'], "black")
        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx != 0 or dy != 0:  # Skip the center position
                    draw.text((x + dx, y + dy), away_abr, font=self.font_big, fill=away_secondary_color)
        # Draw the main text
        draw.text((x,y), away_abr, font=self.font_big, fill=away_color)
        
        # Home team abbreviation with outline
        x, y = self.get_centered_text_xy(draw, home_abr, self.font_big, (640, 40))
        home_secondary_color = self.team_secondary_colors.get(game_data['home_team'], "black")
        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx != 0 or dy != 0:  # Skip the center position
                    draw.text((x + dx, y + dy), home_abr, font=self.font_big, fill=home_secondary_color)
        # Draw the main text
        draw.text((x, y), home_abr, font=self.font_big, fill=home_color)
        
        # DEBUG: Draw position markers to help find correct coordinates
        # Uncomment these lines to see where text is being placed
        # draw.rectangle([75, 45, 85, 55], fill="red")  # Away team position
        # draw.rectangle([self.width-285, 45, self.width-275, 55], fill="blue")  # Home team position
        
        # Draw VS centered between team abbreviations
        # draw.text((self.width//2-40, 120), "VS", font=self.font_vs, fill=self.text_color)
        
        # Game date and venue info - centered below VS
        game_date = game_data.get('game_date', 'TBD')
        venue = game_data.get('venue', 'TBD')
        location = game_data.get('location', 'TBD')
        
        x, y = self.get_centered_text_xy(draw, game_date, self.font_mid, (400, 40))
        draw.text((x, 100), game_date, font=self.font_mid, fill=self.text_color)
        x, y = self.get_centered_text_xy(draw, venue, self.font_mid, (400, 40))
        draw.text((x, 130), venue, font=self.font_mid, fill=self.text_color)
        x, y = self.get_centered_text_xy(draw, location, self.font_mid, (400, 40))
        draw.text((x, 160), location, font=self.font_mid, fill=self.text_color)
        
        # Draw lineups - just the text, no table drawing
        away_lineup = game_data.get('away_lineup', [])
        home_lineup = game_data.get('home_lineup', [])
        
        # Define positions for text (you'll need to adjust these to match your template)
        YvalTopCell = 250
        row_h = 78
        
        # Pitcher names with separate SP label and name fields
        away_sp = game_data.get('away_pitcher', 'TBD')
        home_sp = game_data.get('home_pitcher', 'TBD')

        x, y = self.get_centered_text_xy(draw, "SP", self.font_reg, (55, YvalTopCell))
        draw.text((x, y), "SP", font=self.font_reg, fill="black")

        x, y = self.get_centered_text_xy(draw, away_sp, self.font_bold, (260, YvalTopCell))
        draw.text((x, y), away_sp, font=self.font_bold, fill="black")

        x, y = self.get_centered_text_xy(draw, "SP", self.font_reg, (455, YvalTopCell))
        draw.text((x, y), "SP", font=self.font_reg, fill="black")

        x, y = self.get_centered_text_xy(draw, home_sp, self.font_bold, (660, YvalTopCell))
        draw.text((x, y), home_sp, font=self.font_bold, fill="black")
        
        # Draw lineup text only
        for i in range(9):
            y = (YvalTopCell+45) + row_h*(i)
            
            # Away team lineup (left column)
            if i < len(away_lineup):
                player = away_lineup[i]
                pos = player.get('position', '')
                name = player.get('name', '')
                x, n = self.get_centered_text_xy(draw, pos, self.font_reg, (55, 40))
                draw.text((x, y+22), pos, font=self.font_reg, fill="black")
                x, n = self.get_centered_text_xy(draw, name, self.font_bold, (260, 40))
                draw.text((x, y+22), name, font=self.font_bold, fill="black")
            
            # Home team lineup (right column)
            if i < len(home_lineup):
                player = home_lineup[i]
                pos = player.get('position', '')
                name = player.get('name', '')
                x, n = self.get_centered_text_xy(draw, pos, self.font_reg, (455, 40))
                draw.text((x, y+22), pos, font=self.font_reg, fill="black")
                x, n = self.get_centered_text_xy(draw, name, self.font_bold, (660, 40))
                draw.text((x, y+22), name, font=self.font_bold, fill="black")
        
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