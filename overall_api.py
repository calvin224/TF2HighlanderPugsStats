# app/api/overall_api.py
from .base_api import PlayerClassStatsAPI

class OverallStatsAPI(PlayerClassStatsAPI):
    def __init__(self):
        super().__init__("overall", "overall_player_stats")
        super().__init__("overall_30days", "overall_player_stats_30days")