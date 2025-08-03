# MLBMatchupXBot
This repository is for an X (Twitter) bot that posts daily Major League Baseball (MLB) Matchup data with modern visual design and player performance indicators.

Here is a link to the X profile: https://x.com/MLB_Matchup_Bot

## Features
- **Automated Daily Lineup Posts**: Starting lineups for all MLB games posted when lineup cards are submitted
- **Complete Game Info**: Batting order, positions, starting pitchers, team records, and game details
- **Player Performance Stats**: Current season batting averages, home runs, RBIs, and pitcher ERA/W-L records
- **Performance Indicators**: Visual color coding for hot/cold player performance
- **Modern Image Design**: Clean layout with team colors and professional styling

## How It Works
The bot monitors MLB games daily and generates lineup images when official lineups are released. Each image includes:
- Starting lineups with batting order and positions
- Player statistics (AVG, HR, RBI for batters; W-L, ERA for pitchers)
- Team records and game information
- Visual performance indicators (red outlines for hot players, blue for cold)

## Testing
Use `test_single_game.py` to test the image generation with a single game from today's schedule.
