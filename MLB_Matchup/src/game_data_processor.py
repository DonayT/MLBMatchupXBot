from MLB_API_Client import MLBAPIClient

class GameDataProcessor:
    def __init__(self):
        self.mlb_api_client = MLBAPIClient()

    """
    params: game (dict) - Game dictionary from MLB schedule containing game information
    returns: dict - Complete game data including lineups, pitchers, venue, and lineup status
    summary: Process raw game data and extract comprehensive game information including player lineups and stats
    """
    def get_game_data(self, game):
        game_id = game['game_id']
        home = game['home_name']
        away = game['away_name']
        
        home_team_id = game.get('home_id', 119)
        away_team_id = game.get('away_id', 119)
        
        boxscore = self.mlb_api_client.get_boxscore(game_id)
        
        home_pitcher = game.get('home_probable_pitcher') or 'TBD'
        away_pitcher = game.get('away_probable_pitcher') or 'TBD'

        game_datetime = game.get('game_datetime', '')
        game_date = game.get('game_date', '')

        venue_id = game.get('venue_id')
        venue = self.mlb_api_client.get_venue_data(venue_id)
        venue_name = venue.get('name', 'Unknown Venue') if venue else 'Unknown Venue'
        city, state = self.mlb_api_client.get_venue_location(venue_name)

        formatted_date, formatted_time = self.mlb_api_client.format_game_datetime(game_datetime, game_date)

        game_data = {
            'game_id': game_id,
            'home_team': home,
            'away_team': away,
            'home_pitcher': home_pitcher,
            'away_pitcher': away_pitcher,
            'game_date': formatted_date,
            'game_time': formatted_time,
            'home_lineup': [],
            'away_lineup': [],
            'home_pitchers': [],
            'away_pitchers': [],
            'venue': venue_name,
            'city': city,
            'state': state,
            'lineups_official': self.mlb_api_client.are_lineups_official(boxscore)
        }
        
        if game_data['lineups_official']:
            print(f"   Lineups official - fetching player stats...")
            game_data['home_lineup'] = self.mlb_api_client.extract_lineup_data(boxscore, 'home', home_team_id)
            game_data['away_lineup'] = self.mlb_api_client.extract_lineup_data(boxscore, 'away', away_team_id)
            game_data['home_pitchers'] = self.mlb_api_client.extract_pitcher_data(boxscore, 'home', home_team_id)
            game_data['away_pitchers'] = self.mlb_api_client.extract_pitcher_data(boxscore, 'away', away_team_id)
        else:
            print(f"   Lineups not official - skipping player stats...")
            game_data['home_lineup'] = self.mlb_api_client.extract_lineup_data_basic(boxscore, 'home')
            game_data['away_lineup'] = self.mlb_api_client.extract_lineup_data_basic(boxscore, 'away')
            game_data['home_pitchers'] = self.mlb_api_client.extract_pitcher_data_basic(boxscore, 'home')
            game_data['away_pitchers'] = self.mlb_api_client.extract_pitcher_data_basic(boxscore, 'away')
    
        return game_data

    

