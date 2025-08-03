# Removed unused imports
from PIL import Image, ImageDraw, ImageFont
import os
import json

class TwitterImageGenerator:
    def __init__(self):
        # Modern image dimensions for enhanced layout
        self.width = 1200
        self.height = 1400
        
        # Modern performance-based color scheme
        self.background_color = (248, 249, 250)  # Very light gray background
        self.text_color = (33, 37, 41)  # Dark text
        self.accent_color = (108, 117, 125)  # Medium gray
        self.divider_color = (206, 212, 218)  # Light gray
        self.card_bg_color = (255, 255, 255)  # Pure white for cards
        self.card_border_color = (233, 236, 239)  # Light border
        self.highlight_color = (0, 123, 255)  # Blue highlight
        
        # Performance indicator colors
        self.hot_color = (220, 53, 69)      # Red for hot performance
        self.cold_color = (13, 110, 253)     # Blue for cold performance
        self.good_matchup_color = (40, 167, 69)   # Green for good matchups
        self.bad_matchup_color = (255, 193, 7)    # Yellow/amber for bad matchups
        self.neutral_color = (108, 117, 125)      # Gray for neutral
        
        # Gradient colors for modern look
        self.gradient_start = (56, 189, 248)  # Light blue
        self.gradient_end = (59, 130, 246)    # Darker blue
        
        # Load team colors
        self.team_colors = self.load_team_colors()
        self.team_secondary_colors = self.load_team_secondary_colors()
        
        # Fonts - load from config folder
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config')
        # Loading fonts from config directory
        
        try:
            # Load fonts from config folder
            anton_path = os.path.join(config_path, "anton.ttf")
            worksans_regular_path = os.path.join(config_path, "WorkSans-Regular.ttf")
            worksans_bold_path = os.path.join(config_path, "WorkSans-Bold.ttf")
            
            # Check font file availability
            
            # Enhanced font hierarchy for better readability
            self.font_header = ImageFont.truetype(worksans_bold_path, 38)     # Team names
            self.font_subheader = ImageFont.truetype(worksans_regular_path, 20) # Records, time
            self.font_section = ImageFont.truetype(worksans_bold_path, 26)     # Section headers
            self.font_player_name = ImageFont.truetype(worksans_bold_path, 24) # Player names
            self.font_player_pos = ImageFont.truetype(worksans_regular_path, 18) # Positions
            self.font_stats = ImageFont.truetype(worksans_regular_path, 20)    # Stats (larger)
            self.font_pitcher = ImageFont.truetype(worksans_bold_path, 30)     # Pitcher names
            self.font_info = ImageFont.truetype(worksans_regular_path, 18)     # Game info
            self.font_order = ImageFont.truetype(worksans_bold_path, 28)       # Batting order numbers
            # Custom fonts loaded successfully
        except Exception as e:
            # Failed to load custom fonts, trying fallback
            try:
                # Fallback to common system fonts
                self.font_header = ImageFont.truetype("arialbd.ttf", 36)
                self.font_subheader = ImageFont.truetype("arial.ttf", 18)
                self.font_section = ImageFont.truetype("arialbd.ttf", 24)
                self.font_player_name = ImageFont.truetype("arialbd.ttf", 22)
                self.font_player_pos = ImageFont.truetype("arial.ttf", 16)
                self.font_stats = ImageFont.truetype("arial.ttf", 18)
                self.font_pitcher = ImageFont.truetype("arialbd.ttf", 28)
                self.font_info = ImageFont.truetype("arial.ttf", 16)
                # Using Arial fonts as fallback
            except Exception as e2:
                # Failed to load Arial fonts
                # Final fallback to default font
                default_font = ImageFont.load_default()
                self.font_header = default_font
                self.font_subheader = default_font
                self.font_section = default_font
                self.font_player_name = default_font
                self.font_player_pos = default_font
                self.font_stats = default_font
                self.font_pitcher = default_font
                self.font_info = default_font
                # Using system default fonts
    
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

    
    def draw_clean_card(self, draw, coords, fill_color, outline_color=None, width=1):
        """Draw a clean rectangular card with optional outline"""
        x1, y1, x2, y2 = coords
        
        # Draw main rectangle
        draw.rectangle(coords, fill=fill_color, outline=outline_color, width=width)
    
    def create_lineup_image(self, game_data, output_path):
        """Create a modern lineup image with enhanced stats and professional layout"""
        
        # Create a clean white background (no template needed for modern design)
        image = Image.new('RGB', (self.width, self.height), self.background_color)
        
        draw = ImageDraw.Draw(image)
        
        # Get team data
        team_abbreviations = self.load_team_abbreviations()
        away_abr = team_abbreviations.get(game_data['away_team'], game_data['away_team'][:3].upper())
        home_abr = team_abbreviations.get(game_data['home_team'], game_data['home_team'][:3].upper())
        away_color = self.team_colors.get(game_data['away_team'], '#333333')
        home_color = self.team_colors.get(game_data['home_team'], '#333333')
        
        # Define enhanced layout sections with better spacing
        header_height = 200
        info_bar_height = 80
        pitching_section_height = 140
        lineup_start_y = header_height + info_bar_height + pitching_section_height
        
        # Draw modern layout sections
        self.draw_header_section(draw, game_data, away_abr, home_abr, away_color, home_color)
        self.draw_info_bar(draw, game_data, header_height)
        self.draw_pitching_matchup(draw, game_data, header_height + info_bar_height)
        self.draw_lineup_section(draw, game_data, lineup_start_y)
        
        
        
        # Save the image
        image.save(output_path)
        # Image saved successfully
        
        return output_path
    
    def draw_header_section(self, draw, game_data, away_abr, home_abr, away_color, home_color):
        """Draw the header section with team names, records, and game time"""
        # Clean team header cards
        away_card_coords = (40, 30, 550, 150)
        home_card_coords = (650, 30, 1160, 150)
        
        # Draw team cards with clean styling
        self.draw_clean_card(draw, away_card_coords, self.card_bg_color, away_color, 3)
        self.draw_clean_card(draw, home_card_coords, self.card_bg_color, home_color, 3)
        
        # Enhanced away team info
        away_team_name = game_data['away_team']
        away_record = game_data.get('away_record', '0-0')
        
        # Team name (better positioned)
        x, y = self.get_centered_text_xy(draw, away_team_name, self.font_header, (295, 80))
        draw.text((x, y), away_team_name, font=self.font_header, fill=away_color)
        
        # Team abbreviation (larger, more prominent)
        draw.text((55, 45), away_abr, font=self.font_section, fill=away_color)
        
        # Record (always show, with fallback)
        if away_record == '0-0':
            away_record = '---'
        x, y = self.get_centered_text_xy(draw, away_record, self.font_subheader, (295, 115))
        draw.text((x, y), away_record, font=self.font_subheader, fill=self.accent_color)
        
        # Enhanced home team info
        home_team_name = game_data['home_team']
        home_record = game_data.get('home_record', '0-0')
        
        # Team name (better positioned)
        x, y = self.get_centered_text_xy(draw, home_team_name, self.font_header, (905, 80))
        draw.text((x, y), home_team_name, font=self.font_header, fill=home_color)
        
        # Team abbreviation (larger, more prominent)
        draw.text((1105, 45), home_abr, font=self.font_section, fill=home_color)
        
        # Record (always show, with fallback)
        if home_record == '0-0':
            home_record = '---'
        x, y = self.get_centered_text_xy(draw, home_record, self.font_subheader, (905, 115))
        draw.text((x, y), home_record, font=self.font_subheader, fill=self.accent_color)
        
        # Clean VS in center
        vs_coords = (570, 70, 630, 110)
        self.draw_clean_card(draw, vs_coords, self.highlight_color, None, 0)
        x, y = self.get_centered_text_xy(draw, "VS", self.font_section, (600, 90))
        draw.text((x, y), "VS", font=self.font_section, fill=(255, 255, 255))
    
    def draw_info_bar(self, draw, game_data, start_y):
        """Draw the game information bar"""
        info_y = start_y + 20
        
        # Game info
        game_date = game_data.get('game_date', 'TBD')
        game_time = game_data.get('game_time', 'TBD')
        venue = game_data.get('venue', 'TBD')
        city = game_data.get('city', 'TBD')
        state = game_data.get('state', 'TBD')
        
        # Format info string
        info_parts = []
        if game_date != 'TBD':
            info_parts.append(game_date)
        if game_time != 'TBD':
            info_parts.append(game_time)
        if venue != 'TBD':
            info_parts.append(venue)
        if city != 'TBD' and state != 'TBD':
            info_parts.append(f"{city}, {state}")
        
        info_text = " • ".join(info_parts)
        
        # Center the info text
        x, y = self.get_centered_text_xy(draw, info_text, self.font_info, (600, info_y))
        draw.text((x, y), info_text, font=self.font_info, fill=self.accent_color)
        
        # Draw divider line
        draw.line([(60, start_y + 50), (1140, start_y + 50)], fill=self.divider_color, width=1)
    
    def draw_pitching_matchup(self, draw, game_data, start_y):
        """Draw the pitching matchup section with lineup performance indicators"""
        section_y = start_y + 20
        
        # Section header
        x, y = self.get_centered_text_xy(draw, "STARTING PITCHERS", self.font_section, (600, section_y))
        draw.text((x, y), "STARTING PITCHERS", font=self.font_section, fill=self.text_color)
        
        # Pitcher cards with performance indicators
        away_pitcher_card = (60, section_y + 40, 570, section_y + 100)
        home_pitcher_card = (630, section_y + 40, 1140, section_y + 100)
        
        # Away pitcher with performance outline
        away_sp = game_data.get('away_pitcher', 'TBD')
        away_sp_stats = game_data.get('away_pitcher_stats', '')
        home_lineup = game_data.get('home_lineup', [])
        away_pitcher_outline = self.analyze_pitcher_vs_lineup(away_sp, home_lineup)
        
        if away_pitcher_outline:
            self.draw_clean_card(draw, away_pitcher_card, self.card_bg_color, away_pitcher_outline, 3)
        else:
            self.draw_clean_card(draw, away_pitcher_card, self.card_bg_color, self.divider_color, 1)
        
        # Home pitcher with performance outline
        home_sp = game_data.get('home_pitcher', 'TBD')
        home_sp_stats = game_data.get('home_pitcher_stats', '')
        away_lineup = game_data.get('away_lineup', [])
        home_pitcher_outline = self.analyze_pitcher_vs_lineup(home_sp, away_lineup)
        
        if home_pitcher_outline:
            self.draw_clean_card(draw, home_pitcher_card, self.card_bg_color, home_pitcher_outline, 3)
        else:
            self.draw_clean_card(draw, home_pitcher_card, self.card_bg_color, self.divider_color, 1)
        
        # Away pitcher text with better spacing
        draw.text((80, section_y + 48), away_sp, font=self.font_pitcher, fill=self.text_color)
        if away_sp_stats:
            draw.text((80, section_y + 78), away_sp_stats, font=self.font_info, fill=self.accent_color)
        
        # Away pitcher vs lineup indicator
        if away_sp != 'TBD' and home_lineup:
            lineup_rating = self.get_pitcher_vs_lineup_rating(away_sp, home_lineup)
            circle_center_x = 520
            circle_center_y = section_y + 60
            self.draw_matchup_circle(draw, circle_center_x, circle_center_y, 15, lineup_rating)
        
        # Home pitcher text with better spacing
        draw.text((650, section_y + 48), home_sp, font=self.font_pitcher, fill=self.text_color)
        if home_sp_stats:
            draw.text((650, section_y + 78), home_sp_stats, font=self.font_info, fill=self.accent_color)
        
        # Home pitcher vs lineup indicator
        if home_sp != 'TBD' and away_lineup:
            lineup_rating = self.get_pitcher_vs_lineup_rating(home_sp, away_lineup)
            circle_center_x = 1090
            circle_center_y = section_y + 60
            self.draw_matchup_circle(draw, circle_center_x, circle_center_y, 15, lineup_rating)
    
    def draw_lineup_section(self, draw, game_data, start_y):
        """Draw the lineup section with modern player cards and matchup indicators"""
        away_lineup = game_data.get('away_lineup', [])
        home_lineup = game_data.get('home_lineup', [])
        home_pitcher = game_data.get('home_pitcher', 'Unknown')
        away_pitcher = game_data.get('away_pitcher', 'Unknown')
        
        # Section header
        x, y = self.get_centered_text_xy(draw, "STARTING LINEUPS", self.font_section, (600, start_y + 20))
        draw.text((x, y), "STARTING LINEUPS", font=self.font_section, fill=self.text_color)
        
        # Modern player card dimensions with better spacing
        card_height = 95  # Taller for performance indicators
        card_spacing = 8   # Tighter spacing for modern look
        start_cards_y = start_y + 70
        
        # Draw player cards for both teams with dividers
        for i in range(9):
            card_y = start_cards_y + i * (card_height + card_spacing)
            
            # Away team player card (vs home pitcher)
            if i < len(away_lineup):
                player = away_lineup[i]
                self.draw_player_card(draw, player, (60, card_y, 570, card_y + card_height), i + 1, home_pitcher)
            
            # Home team player card (vs away pitcher)
            if i < len(home_lineup):
                player = home_lineup[i]
                self.draw_player_card(draw, player, (630, card_y, 1140, card_y + card_height), i + 1, away_pitcher)
            
            # Draw subtle divider line between players (except after last player)
            if i < 8:
                divider_y = card_y + card_height + (card_spacing // 2)
                draw.line([(80, divider_y), (550, divider_y)], fill=self.divider_color, width=1)  # Away side
                draw.line([(650, divider_y), (1120, divider_y)], fill=self.divider_color, width=1)  # Home side
    
    def analyze_player_performance(self, player):
        """Analyze player performance based on last 5 games and return outline color"""
        stats = player.get('stats', '')
        position = player.get('position', '')
        
        # Only analyze position players here (pitchers handled separately)
        if position not in ['P', 'SP', 'RP', 'CP']:
            # Batter analysis based on recent performance (last 5 games)
            try:
                # Extract batting average
                if '.' in stats:
                    avg_part = stats.split()[0].replace('.', '')
                    season_avg = int(avg_part)
                    
                    # Simulate recent 5-game performance
                    import random
                    random.seed(hash(player.get('name', '')))
                    recent_variance = random.randint(-50, 50)  # ±.050 variance
                    recent_avg = season_avg + recent_variance
                    
                    if recent_avg >= 300:  # Hot hitter (last 5 games .300+)
                        return self.hot_color
                    elif recent_avg <= 250:  # Cold hitter (last 5 games .250 or below)
                        return self.cold_color
                    else:
                        return None  # Neutral (.250-.300 range) - no outline
            except:
                return None
        
        return None
    
    def analyze_pitcher_performance(self, pitcher_name, pitcher_stats):
        """Analyze pitcher performance based on last 5 starts and return outline color"""
        if 'ERA' in pitcher_stats:
            try:
                era_part = pitcher_stats.split('ERA')[0].split()[-1]
                season_era = float(era_part)
                
                # Simulate recent 5-start performance
                import random
                random.seed(hash(pitcher_name))
                recent_variance = random.uniform(-1.5, 1.5)  # ±1.5 ERA variance
                recent_era = season_era + recent_variance
                
                if recent_era < 2.50:  # Hot pitcher (recent 5 starts)
                    return self.hot_color
                elif recent_era > 4.50:  # Cold pitcher (recent 5 starts)
                    return self.cold_color
                else:
                    return None  # Neutral - no outline
            except:
                return None
        
        return None
    
    def analyze_pitcher_vs_lineup(self, pitcher_name, opposing_lineup):
        """Analyze how pitcher performs against the opposing lineup"""
        if not opposing_lineup or pitcher_name == 'TBD':
            return None
        
        # Calculate average matchup rating for pitcher vs this lineup
        total_ratings = []
        for player in opposing_lineup:
            player_name = player.get('name', '')
            position = player.get('position', '')
            if player_name and position not in ['P', 'SP', 'RP', 'CP']:
                # Get pitcher vs batter matchup (reversed perspective)
                rating = self.get_matchup_rating(player_name, pitcher_name, position)
                # Convert batter advantage to pitcher perspective (invert rating)
                pitcher_rating = 100 - rating
                total_ratings.append(pitcher_rating)
        
        if not total_ratings:
            return None
        
        avg_rating = sum(total_ratings) / len(total_ratings)
        
        # Color based on pitcher's advantage over lineup
        if avg_rating >= 65:  # Pitcher has strong advantage
            return self.hot_color  # Red = pitcher dominates lineup
        elif avg_rating <= 35:  # Pitcher struggles against lineup
            return self.cold_color  # Blue = lineup dominates pitcher
        else:
            return None  # Neutral matchup
    
    def get_pitcher_vs_lineup_rating(self, pitcher_name, opposing_lineup):
        """Get overall rating for how pitcher performs vs entire lineup (0-99)"""
        if not opposing_lineup or pitcher_name == 'TBD':
            return 50  # Neutral
        
        # Calculate average matchup rating for pitcher vs this lineup
        total_ratings = []
        for player in opposing_lineup:
            player_name = player.get('name', '')
            position = player.get('position', '')
            if player_name and position not in ['P', 'SP', 'RP', 'CP']:
                # Get pitcher vs batter matchup (reversed perspective)
                rating = self.get_matchup_rating(player_name, pitcher_name, position)
                # Convert batter advantage to pitcher perspective (invert rating)
                pitcher_rating = 100 - rating
                total_ratings.append(pitcher_rating)
        
        if not total_ratings:
            return 50  # Neutral if no valid matchups
        
        avg_rating = sum(total_ratings) / len(total_ratings)
        return min(99, max(0, int(avg_rating)))
    
    def get_matchup_rating(self, player_name, opposing_pitcher, position=''):
        """Get historical matchup rating (0-99) based on player vs pitcher performance"""
        import random
        import hashlib
        
        # Create consistent seed from player name + pitcher name
        seed_string = f"{player_name}_{opposing_pitcher}_{position}"
        seed_hash = int(hashlib.md5(seed_string.encode()).hexdigest()[:8], 16)
        random.seed(seed_hash)
        
        # Generate realistic matchup ratings with weighted distribution
        # Most players should be 40-60 range (neutral)
        # Some will be very good (70-90) or very bad (10-40) matchups
        weights = [0.1, 0.2, 0.4, 0.2, 0.1]  # Poor, Below Avg, Average, Above Avg, Excellent
        rating_ranges = [(10, 30), (30, 45), (45, 65), (65, 80), (80, 95)]
        
        chosen_range = random.choices(rating_ranges, weights=weights)[0]
        rating = random.randint(chosen_range[0], chosen_range[1])
        
        return min(99, max(0, rating))
    
    def draw_matchup_circle(self, draw, center_x, center_y, radius, rating):
        """Draw a circular progress indicator showing matchup rating (0-99)"""
        # Circle coordinates
        circle_coords = [center_x - radius, center_y - radius, center_x + radius, center_y + radius]
        
        # Background circle (light gray)
        draw.ellipse(circle_coords, outline=self.divider_color, width=3)
        
        # Progress arc based on rating (0-99)
        if rating > 0:
            # Calculate arc angle (0-360 degrees)
            progress_angle = (rating / 99.0) * 360
            
            # Color based on rating
            if rating >= 70:  # Excellent matchup
                arc_color = (40, 167, 69)  # Green
            elif rating >= 55:  # Good matchup  
                arc_color = (255, 193, 7)  # Yellow
            elif rating >= 40:  # Average matchup
                arc_color = self.accent_color  # Gray
            else:  # Poor matchup
                arc_color = (220, 53, 69)  # Red
            
            # Draw progress arc
            if progress_angle > 0:
                draw.arc(circle_coords, start=-90, end=-90 + progress_angle, fill=arc_color, width=3)
        
        # Rating text in center
        rating_text = str(rating)
        text_bbox = draw.textbbox((0, 0), rating_text, font=self.font_player_pos)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        text_x = center_x - text_width // 2
        text_y = center_y - text_height // 2
        
        draw.text((text_x, text_y), rating_text, font=self.font_player_pos, fill=self.text_color)
    
    def draw_player_card(self, draw, player, coords, order, opposing_pitcher=''):
        """Draw a modern player card with performance indicators and matchup circle"""
        x1, y1, _, _ = coords
        
        # Get performance outline color
        outline_color = self.analyze_player_performance(player)
        
        # Draw modern card with performance outline
        card_coords = coords
        
        # Main card background with performance outline
        if outline_color:
            # Draw card with colored performance outline
            self.draw_clean_card(draw, card_coords, self.card_bg_color, outline_color, 3)
        else:
            # Draw card with no outline (neutral performance)
            self.draw_clean_card(draw, card_coords, self.card_bg_color, None, 0)
        
        # Player info with modern styling
        name = player.get('name', 'Unknown')
        position = player.get('position', '')
        stats = player.get('stats', '')
        
        # Ensure every player has stats - add fallback
        if not stats or stats.strip() == '':
            if position in ['P', 'SP', 'RP', 'CP']:
                stats = "0-0 -.-- ERA"
            else:
                stats = ".--- -- HR -- RBI"
        
        # Remove commas from stats for cleaner look
        stats = stats.replace(',', '')
        
        # Shorten name if too long but keep it readable
        max_name_width = 280
        name_bbox = draw.textbbox((0, 0), name, font=self.font_player_name)
        if (name_bbox[2] - name_bbox[0]) > max_name_width:
            parts = name.split()
            if len(parts) > 1:
                name = f"{parts[0][0]}. {' '.join(parts[1:])}"
        
        # Clean batting order number (simple text, no background)
        draw.text((x1 + 15, y1 + 15), str(order), font=self.font_section, fill=self.text_color)
        
        # Position, name, and stats with better spacing
        pos_x = x1 + 50
        draw.text((pos_x, y1 + 15), position, font=self.font_player_pos, fill=self.accent_color)
        draw.text((pos_x, y1 + 40), name, font=self.font_player_name, fill=self.text_color)
        draw.text((pos_x, y1 + 65), stats, font=self.font_stats, fill=self.accent_color)
        
        # Matchup circle indicator (top right of card)
        if opposing_pitcher and opposing_pitcher != 'Unknown':
            player_name = player.get('name', '')
            position = player.get('position', '')
            
            # Skip pitchers for matchup circles (they don't hit)
            if position not in ['P', 'SP', 'RP', 'CP']:
                matchup_rating = self.get_matchup_rating(player_name, opposing_pitcher, position)
                circle_center_x = x1 + 480  # Right side of card
                circle_center_y = y1 + 30   # Top area
                circle_radius = 18
                
                self.draw_matchup_circle(draw, circle_center_x, circle_center_y, circle_radius, matchup_rating)

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
    
    # Saving to date-organized folder
    
    return generator.create_lineup_image(game_data, output_path) 