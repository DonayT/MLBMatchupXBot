from MLB_API_Client import MLBAPIClient

class GameDataProcessor:
    def __init__(self):
        self.mlb_api_client = MLBAPIClient()

    def get_game_data(self, game):
        game_id = game['game_id']
        home = game['home_name']
        away = game['away_name']
        
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
            'venue': venue_name,
            'city': city,
            'state': state,
            'lineups_official': self.mlb_api_client.are_lineups_official(boxscore)
        }
        
        game_data['home_lineup'] = self.mlb_api_client.extract_lineup_data(boxscore, 'home')
        game_data['away_lineup'] = self.mlb_api_client.extract_lineup_data(boxscore, 'away')
    
        return game_data

    

