# MLBMatchupXBot

<div align="center">
  <img src="MLB_Matchup/images/logo/MLBMatchupBotLogo.png" alt="MLBMatchupXBot Logo" width="200"/>
  <br>
  <em>Automated MLB Lineup Cards with Enhanced Statistics</em>
</div>

An automated X (Twitter) bot that posts daily Major League Baseball (MLB) lineup cards with enhanced statistics and modern design.

**X Profile**: https://x.com/MLB_Matchup_Bot

**Automation**: Powered by [cron-job.org](https://cron-job.org) and [GitHub Actions](https://github.com/features/actions) for reliable scheduled posting

## 🏟️ Features

- **Automated Lineup Detection**: Monitors MLB games for official lineup submissions
- **Enhanced Statistics**: Integrates player stats and team records using pybaseball
- **Modern Design**: Professional lineup cards with team colors and custom fonts
- **Queue System**: Prevents duplicate posts and tracks processed games
- **Modular Architecture**: Clean separation of concerns for maintainability
- **Fallback System**: Mock data support for testing and development

## 🏗️ Project Structure

```
MLBMatchupXBot/
├── MLB_Matchup/
│   ├── src/
│   │   ├── Main.py                    # Main orchestrator
│   │   ├── MLBMatchup.py              # Entry point wrapper
│   │   ├── game_data_processor.py     # Game data extraction
│   │   ├── game_queue.py              # Queue management
│   │   ├── twitter_image_generator.py # Image creation
│   │   ├── MLB_API_Client.py          # MLB API integration
│   │   ├── get_stats.py               # Statistics module
│   │   ├── date_organizer.py          # Date/file management
│   │   ├── lineup_validator.py        # Lineup validation
│   │   ├── get_address.py             # Venue information
│   │   └── test_image_generator.py    # Testing utilities
│   ├── config/
│   │   ├── mock_game_data.py          # Test data
│   │   ├── teamPrimaryColors.json     # Team color schemes
│   │   ├── teamSecondaryColors.json   # Secondary colors
│   │   ├── teamAbreviations.json      # Team abbreviations
│   │   ├── teamHashtags.json          # Team hashtags
│   │   ├── teamVenues.json            # Venue information
│   │   ├── stateAbbreviations.json    # State codes
│   │   └── static/                    # Font files
│   ├── data/
│   │   ├── processed_games.json       # Queue tracking
│   │   └── last_processed_date.txt    # Date tracking
│   └── images/                        # Generated lineup cards
├── Xbot/
│   └── bot.py                         # Twitter upload module
└── requirements.txt                    # Dependencies
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MLB Stats API access
- Twitter API credentials

### Installation
```bash
git clone https://github.com/yourusername/MLBMatchupXBot.git
cd MLBMatchupXBot
pip install -r requirements.txt
```

### Configuration
1. Set up Twitter API credentials in `Xbot/bot.py`
2. Configure MLB API settings in `MLB_Matchup/src/MLB_API_Client.py`
3. Customize team colors and hashtags in `MLB_Matchup/config/`

### Running the Bot
```bash
# Run the main bot
python MLB_Matchup/src/MLBMatchup.py

# Test image generation
python MLB_Matchup/src/test_image_generator.py
```

### Automation Setup
The bot uses multiple automation strategies for reliability:

#### cron-job.org
- **Schedule**: Runs every 15 minutes during MLB season
- **Endpoint**: `https://your-deployment-url.com/trigger`
- **Monitoring**: Email notifications for failures

#### GitHub Actions
- **Schedule**: Runs every 30 minutes via GitHub Actions cron
- **Workflow**: `.github/workflows/mlb-bot.yml`
- **Fallback**: Automatic retry on failures
- **Logs**: Available in GitHub Actions tab

## 🔧 Architecture

### Core Modules

- **Main.py**: Orchestrates the entire process flow
- **game_data_processor.py**: Extracts and processes game information
- **twitter_image_generator.py**: Creates professional lineup cards
- **get_stats.py**: Handles player statistics and team records
- **game_queue.py**: Manages processed games to prevent duplicates

### Key Features

- **Modular Design**: Each component has a single responsibility
- **Error Handling**: Graceful fallbacks for API failures
- **Caching**: Optimized API calls with intelligent caching
- **Testing**: Comprehensive test suite with mock data support

## 📊 Data Sources

- **MLB Stats API**: Game schedules, lineups, and player data
- **pybaseball**: Enhanced player statistics and team records
- **Custom Config**: Team colors, hashtags, and venue information

## 🎨 Image Generation

The bot creates professional lineup cards featuring:
- Team abbreviations with custom fonts
- Player names, positions, and batting order
- Starting pitcher information
- Team records and player statistics
- Venue and game time details
- Team-specific color schemes

## 🔄 Workflow

1. **Schedule Check**: Retrieves today's MLB games
2. **Lineup Monitoring**: Waits for official lineup submissions
3. **Data Processing**: Extracts game data and player stats
4. **Image Generation**: Creates professional lineup cards
5. **Queue Management**: Tracks processed games
6. **Twitter Upload**: Posts images with game information

## 🧪 Testing

```bash
# Test with mock data
python MLB_Matchup/src/test_image_generator.py

# Test specific components
python MLB_Matchup/src/debug_team_records.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📝 License
If you use or modify this code, please credit the original authors in your documentation, README, or software credits.

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- MLB Stats API for game data
- pybaseball library for enhanced statistics
- Twitter API for social media integration
- Custom font designers for professional typography

---

**Note**: This bot is designed for educational and entertainment purposes. Please respect MLB's terms of service and Twitter's API guidelines.
