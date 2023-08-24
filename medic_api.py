from base_api import PlayerClassStatsAPI
class MedicStatsAPI(PlayerClassStatsAPI):
    def __init__(self):
        super().__init__("medic", "medic_class_stats")
        super().__init__("medic_30days", "medic_class_stats_30days")