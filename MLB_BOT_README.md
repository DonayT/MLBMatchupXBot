# MLB Matchup Bot

This bot automatically monitors MLB games and generates lineup images when both teams have official lineups posted.

## Setup

1. **Install Dependencies**
   ```
   setup_mlb_bot.bat
   ```
   This will install all required Python packages.

## Usage

### Single Run
To run the bot once and check current games:
```
run_mlb_matchup.bat
```

### Continuous Monitoring
To run the bot continuously (checks every 15 minutes):
```
run_mlb_continuous.bat
```

The continuous script will:
- Run every 15 minutes
- Automatically stop when all games for the day are processed
- Restart the next day for new games

## How It Works

1. **Game Detection**: The bot fetches today's MLB schedule using the MLB Stats API
2. **Lineup Monitoring**: It checks if both teams have official lineups posted
3. **Image Generation**: When lineups are official, it creates a Twitter-optimized image
4. **Organization**: Images are saved in date-based folders (e.g., `MLB_Matchup/images/2025-07-30/`)

## Files Generated

- **Lineup Images**: Saved as PNG files in `MLB_Matchup/images/[DATE]/`
- **Processed Games**: Tracked in `MLB_Matchup/data/processed_games.json`
- **Date Tracking**: Managed in `MLB_Matchup/data/last_processed_date.txt`

## Exit Codes

- **Exit 0**: Normal completion (some games processed or waiting for lineups)
- **Exit 42**: All games for the day are complete (continuous script will stop)

## Requirements

- Python 3.6+
- Internet connection for MLB API access
- Windows PowerShell (for continuous script)

## Troubleshooting

- If you get permission errors, run PowerShell as Administrator
- If the continuous script doesn't work, try running `run_mlb_continuous.bat` directly
- Check the console output for any error messages 