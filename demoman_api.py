# app/api/demoman_api.py
from .base_api import PlayerClassStatsAPI

class DemomanStatsAPI(PlayerClassStatsAPI):
    def __init__(self):
        super().__init__("demoman", "demoman_class_stats")
        super().__init__("demoman_30days", "demoman_class_stats_30days")
