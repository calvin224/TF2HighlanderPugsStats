from base_api import PlayerClassStatsAPI

class SniperStatsAPI(PlayerClassStatsAPI):
    def __init__(self):
        super().__init__("sniper", "sniper_class_stats")
        super().__init__("sniper_30days", "sniper_class_stats_30days")
