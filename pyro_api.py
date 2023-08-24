# app/api/pyro_api.py
from .base_api import PlayerClassStatsAPI

class PyroStatsAPI(PlayerClassStatsAPI):
    def __init__(self):
        super().__init__("pyro", "pyro_class_stats")
        super().__init__("pyro_30days", "pyro_class_stats_30days")