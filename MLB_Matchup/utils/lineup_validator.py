class LineupValidator:
    def __init__(self):
        pass

    """
    params: boxscore (dict) - Game boxscore data containing home and away team information
    returns: bool - True if both teams have complete 9-player batting orders, False otherwise
    summary: Check if both home and away teams have official lineups with exactly 9 players
    """
    def are_lineups_official(self, boxscore):
        home_batting_order = boxscore['home'].get('battingOrder', [])
        away_batting_order = boxscore['away'].get('battingOrder', [])
        return len(home_batting_order) == 9 and len(away_batting_order) == 9

    """
    params: lineup (list) - List of player dictionaries representing a team's lineup
    returns: bool - True if lineup has exactly 9 players, False otherwise
    summary: Validate that a single team's lineup is complete with exactly 9 players
    """
    def validate_lineup_complete(self, lineup):
        if not lineup or len(lineup) < 9:
            return False

        positions = [player.get('position', '') for player in lineup]
        return len(positions) == 9 

    """
    params: boxscore (dict) - Game boxscore data containing home and away team information
    returns: dict - Dictionary with lineup counts and completion status for both teams
    summary: Get detailed status of both teams' lineups including counts and completion status
    """
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