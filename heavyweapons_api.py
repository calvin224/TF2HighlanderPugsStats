
from base_api import PlayerClassStatsAPI

class HeavyWeaponsStatsAPI(PlayerClassStatsAPI):
    def __init__(self):
        super().__init__("heavyweapons", "heavyweapons_class_stats")
        super().__init__("heavyweapons_30days", "heavyweapons_class_stats_30days")