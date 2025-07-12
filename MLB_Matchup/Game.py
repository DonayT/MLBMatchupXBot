import statsapi

class Game: 
    def __init__(self, game_id, date):
        self.game_id = game_id
        self.date = date
        self.home_team = None
        self.away_team = None
        self.lineups = {'home': [], 'away': []}

    def grab_boxscore(self):
        boxscore = statsapi.boxscore_data(self.game_id)
        self.home_team = boxscore['teamInfo']['home']['teamName']
        self.away_team = boxscore['teamInfo']['away']['teamName']
        self.lineups['home'] = self.parse_lineups(boxscore['home']['players'])
        self.lineups['away'] = self.parse_lineups(boxscore['away']['players'])

    def parse_lineups(self, players):
        starters = []

        for player in players.values():
            stats = player.get('stats', {})
            order = stats.get('battingOrder')

            if order and int(order) > 0:
                starters.append({
                    'batting_order': int(order),
                    'name': player['person']['fullName'],
                    'position': player['position']['abbreviation']
                })

        return sorted(starters, key = lambda x: x['batting_order'])

