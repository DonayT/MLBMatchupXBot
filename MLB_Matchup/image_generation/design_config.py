"""
Design Configuration for Lineup Cards
Tweak these values to change the appearance without touching HTML/CSS
"""

DESIGN = {
    # Card dimensions
    'card_width': 1200,
    'card_height': 1400,
    'card_padding': '20px 30px 20px 20px',

    # Team abbreviation styling
    'team_font_size': 250,
    'team_font_family': 'Anton',
    'team_letter_spacing': -2,
    'team_stroke_width': 6,
    'team_margin_top': 40,
    'team_vertical_offset': -80,  # Moves team names up/down

    # Stadium/venue styling
    'stadium_font_size': 36,
    'stadium_font_weight': 'bold',
    'stadium_margin_top': 80,

    # Game info (date, time)
    'game_info_font_size': 28,
    'game_info_margin_top': 10,

    # Lineup table styling
    'lineup_header_font_size': 32,
    'lineup_row_font_size': 24,
    'lineup_row_height': 55,
    'lineup_padding': '12px',

    # Player stats styling
    'stats_font_size': 18,
    'stats_opacity': 0.8,

    # Spacing and layout
    'section_spacing': 20,
    'table_margin_top': 30,

    # Colors (defaults - will be overridden by team colors)
    'background_gradient': 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)',
    'text_color': '#ffffff',
    'border_color': 'rgba(255, 255, 255, 0.2)',

    # Visual effects
    'border_radius': 12,
    'box_shadow': '0 8px 32px rgba(0, 0, 0, 0.3)',
    'backdrop_blur': 10,
}

# Font configurations
FONTS = {
    'primary': 'Anton',
    'secondary': 'WorkSans-Bold',
    'body': 'WorkSans-Regular',
}

# Sample data for live preview
SAMPLE_DATA = {
    'away_team': 'TOR',
    'home_team': 'NYM',
    'away_team_full': 'Los Angeles Dodgers',
    'home_team_full': 'New York Yankees',
    'game_date': '08/08/2025',
    'game_time': '7:05 PM ET',
    'game_location': 'Yankee Stadium',
    'away_primary_color': '#005A9C',
    'away_secondary_color': '#FFFFFF',
    'home_primary_color': '#003087',
    'home_secondary_color': '#FFFFFF',
    'away_lineup': [
        {'order': 1, 'name': 'Mookie Betts', 'position': 'RF', 'stats': 'AVG: 0.289 / OPS: 0.872 / H: 7 / RBIs: 4 / SO: 3'},
        {'order': 2, 'name': 'Shohei Ohtani', 'position': 'DH', 'stats': 'AVG: 0.315 / OPS: 1.036 / H: 9 / RBIs: 8 / SO: 2'},
        {'order': 3, 'name': 'Freddie Freeman', 'position': '1B', 'stats': 'AVG: 0.298 / OPS: 0.891 / H: 8 / RBIs: 6 / SO: 1'},
        {'order': 4, 'name': 'Will Smith', 'position': 'C', 'stats': 'AVG: 0.267 / OPS: 0.823 / H: 6 / RBIs: 5 / SO: 4'},
        {'order': 5, 'name': 'Max Muncy', 'position': '3B', 'stats': 'AVG: 0.245 / OPS: 0.798 / H: 5 / RBIs: 7 / SO: 5'},
        {'order': 6, 'name': 'Teoscar Hernandez', 'position': 'LF', 'stats': 'AVG: 0.272 / OPS: 0.845 / H: 7 / RBIs: 6 / SO: 6'},
        {'order': 7, 'name': 'Gavin Lux', 'position': '2B', 'stats': 'AVG: 0.251 / OPS: 0.734 / H: 5 / RBIs: 3 / SO: 3'},
        {'order': 8, 'name': 'Miguel Rojas', 'position': 'SS', 'stats': 'AVG: 0.283 / OPS: 0.712 / H: 6 / RBIs: 2 / SO: 2'},
        {'order': 9, 'name': 'James Outman', 'position': 'CF', 'stats': 'AVG: 0.248 / OPS: 0.701 / H: 4 / RBIs: 3 / SO: 7'},
    ],
    'home_lineup': [
        {'order': 1, 'name': 'Gleyber Torres', 'position': '2B', 'stats': 'AVG: 0.279 / OPS: 0.756 / H: 6 / RBIs: 4 / SO: 4'},
        {'order': 2, 'name': 'Juan Soto', 'position': 'RF', 'stats': 'AVG: 0.288 / OPS: 0.989 / H: 8 / RBIs: 9 / SO: 3'},
        {'order': 3, 'name': 'Aaron Judge', 'position': 'CF', 'stats': 'AVG: 0.301 / OPS: 1.125 / H: 9 / RBIs: 11 / SO: 5'},
        {'order': 4, 'name': 'Giancarlo Stanton', 'position': 'DH', 'stats': 'AVG: 0.243 / OPS: 0.812 / H: 5 / RBIs: 8 / SO: 8'},
        {'order': 5, 'name': 'Anthony Rizzo', 'position': '1B', 'stats': 'AVG: 0.256 / OPS: 0.721 / H: 5 / RBIs: 5 / SO: 6'},
        {'order': 6, 'name': 'DJ LeMahieu', 'position': '3B', 'stats': 'AVG: 0.271 / OPS: 0.698 / H: 6 / RBIs: 3 / SO: 2'},
        {'order': 7, 'name': 'Alex Verdugo', 'position': 'LF', 'stats': 'AVG: 0.265 / OPS: 0.734 / H: 6 / RBIs: 4 / SO: 3'},
        {'order': 8, 'name': 'Jose Trevino', 'position': 'C', 'stats': 'AVG: 0.241 / OPS: 0.645 / H: 4 / RBIs: 2 / SO: 4'},
        {'order': 9, 'name': 'Anthony Volpe', 'position': 'SS', 'stats': 'AVG: 0.258 / OPS: 0.712 / H: 5 / RBIs: 3 / SO: 7'},
    ],
    'away_pitcher': {
        'name': 'Tyler Glasnow',
        'position': 'P',
        'stats': 'ERA: 3.47 WHIP: 0.95 K: 18 IP: 13.0'
    },
    'home_pitcher': {
        'name': 'Gerrit Cole',
        'position': 'P',
        'stats': 'ERA: 2.89 WHIP: 1.02 K: 21 IP: 15.2'
    }
}
