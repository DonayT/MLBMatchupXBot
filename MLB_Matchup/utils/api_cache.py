"""
API Cache Module
Provides caching for MLB API calls to reduce redundant requests
"""

import statsapi
from typing import Optional, Dict, Any

class APICache:
    """
    Cache for MLB API data to minimize redundant API calls
    """
    def __init__(self):
        # Cache player ID lookups
        self._player_id_cache: Dict[str, Optional[int]] = {}

        # Cache boxscore data
        self._boxscore_cache: Dict[int, Dict[str, Any]] = {}

        # Cache team schedules (key: f"{team_id}_{season}")
        self._schedule_cache: Dict[str, list] = {}

    def get_player_id(self, player_name: str) -> Optional[int]:
        """
        Get player ID from cache or lookup from API

        params: player_name (str) - Full name of the player
        returns: int or None - Player ID if found
        """
        # Normalize name for cache key
        cache_key = player_name.lower().strip()

        if cache_key in self._player_id_cache:
            return self._player_id_cache[cache_key]

        # Lookup player from API
        try:
            player_lookup = statsapi.lookup_player(player_name)
            if player_lookup:
                player_id = player_lookup[0]['id']
                self._player_id_cache[cache_key] = player_id
                return player_id
            else:
                self._player_id_cache[cache_key] = None
                return None
        except Exception as e:
            print(f"Error looking up player {player_name}: {e}")
            self._player_id_cache[cache_key] = None
            return None

    def get_boxscore(self, game_id: int) -> Optional[Dict[str, Any]]:
        """
        Get boxscore from cache or fetch from API

        params: game_id (int) - MLB game ID
        returns: dict or None - Boxscore data if found
        """
        if game_id in self._boxscore_cache:
            return self._boxscore_cache[game_id]

        try:
            boxscore = statsapi.boxscore_data(game_id)
            self._boxscore_cache[game_id] = boxscore
            return boxscore
        except Exception as e:
            print(f"Error fetching boxscore for game {game_id}: {e}")
            return None

    def get_team_schedule(self, team_id: int, season: int, start_date: str, end_date: str) -> list:
        """
        Get team schedule from cache or fetch from API

        params: team_id (int) - Team ID
                season (int) - Season year
                start_date (str) - Start date in YYYY-MM-DD format
                end_date (str) - End date in YYYY-MM-DD format
        returns: list - List of games
        """
        cache_key = f"{team_id}_{season}_{start_date}_{end_date}"

        if cache_key in self._schedule_cache:
            return self._schedule_cache[cache_key]

        try:
            schedule = statsapi.schedule(
                team=team_id,
                season=season,
                start_date=start_date,
                end_date=end_date
            )
            self._schedule_cache[cache_key] = schedule
            return schedule
        except Exception as e:
            print(f"Error fetching schedule for team {team_id}: {e}")
            return []

    def clear(self):
        """Clear all caches"""
        self._player_id_cache.clear()
        self._boxscore_cache.clear()
        self._schedule_cache.clear()

    def get_cache_stats(self) -> Dict[str, int]:
        """Get statistics about cache usage"""
        return {
            'player_ids_cached': len(self._player_id_cache),
            'boxscores_cached': len(self._boxscore_cache),
            'schedules_cached': len(self._schedule_cache)
        }


# Global cache instance
_global_cache = APICache()

def get_cache() -> APICache:
    """Get the global cache instance"""
    return _global_cache

def clear_cache():
    """Clear the global cache"""
    _global_cache.clear()
