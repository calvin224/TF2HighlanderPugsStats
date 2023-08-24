from base_api import PlayerClassStatsAPI
class SpyStatsAPI(PlayerClassStatsAPI):
    def __init__(self):
        super().__init__("spy", "spy_class_stats")
        super().__init__("spy_30days", "spy_class_stats_30days")