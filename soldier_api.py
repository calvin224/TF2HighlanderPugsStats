# app/api/soldier_api.py
from base_api import PlayerClassStatsAPI

class SoldierStatsAPI(PlayerClassStatsAPI):
    def __init__(self):
        super().__init__("soldier", "soldier_class_stats")
        super().__init__("soldier_30days", "soldier_class_stats_30days")