class LineupValidator:
    def __init__(self):
        pass

    def are_lineups_official(self, boxscore):
        home_batting_order = boxscore['home'].get('battingOrder', [])
        away_batting_order = boxscore['away'].get('battingOrder', [])
        return len(home_batting_order) == 9 and len(away_batting_order) == 9

    def validate_lineup_complete(self, lineup):
        if not lineup or len(lineup) < 9:
            return False

        positions = [player.get('position', '') for player in lineup]
        return len(positions) == 9 

    def get_lineup_status(self, boxscore):
        home_lineup = boxscore['home'].get('battingOrder', [])
        away_lineup = boxscore['away'].get('battingOrder', [])
        
        return {
            'home_count': len(home_lineup),
            'away_count': len(away_lineup),
            'home_complete': len(home_lineup) == 9,
            'away_complete': len(away_lineup) == 9,
            'both_official': len(home_lineup) == 9 and len(away_lineup) == 9
        }        