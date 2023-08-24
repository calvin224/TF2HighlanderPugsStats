# app/api/soldier_api.py
from base_api import PlayerClassStatsAPI

class EngineerStatsAPI(PlayerClassStatsAPI):
    def __init__(self):
        super().__init__("engineer", "engineer_class_stats")
        super().__init__("engineer_30days", "engineer_class_stats_30days")