from base_api import PlayerClassStatsAPI

class ScoutStatsAPI(PlayerClassStatsAPI):
    def __init__(self):
        super().__init__("scout", "scout_class_stats")
        super().__init__("scout_30days", "scout_class_stats_30days")