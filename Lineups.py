import statsapi
 
game_july_8th_2025 = statsapi.schedule(date='07/08/2025')

## Checking to see if there are any games from this day. 
## Could be off days

if not game_july_8th_2025:
    print("No games found.")
else:
    game = game_july_8th_2025[0]
    game_id = game['game_id']
    home_team = game['home_name']
    away_team = game['away_name']

print(f"Selected game: {away_team} @ {home_team} (Game ID: {game_id})")

## Grabbing the lineups

lineups = statsapi.boxscore_data(game_id)

home_players = lineups['home']['players']
away_players = lineups['away']['players']

def get_starting_lineups(players):
    lineup = []

    for player in players.values():
        stats = player.get('stats', {})
        batting_order = stats.get('battingOrder')
        if batting_order and int(batting_order) > 0:
            lineup.append({
                'order': int(batting_order),
                'name': player['person']['fullname'],
                'position': player['position']['abbreviation']
            })
    
    return sorted(lineup, key = lambda x: x['order'])

print(f"\n{away_team} Starting Lineup:")
for player in get_starting_lineups(away_players):
    print(f"{player['order']}: {player['name']} - {player['position']}")

print(f"\n{home_team} Starting Lineup:")
for player in get_starting_lineups(home_players):
    print(f"{player['order']}: {player['name']} - {player['position']}")




