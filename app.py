from flask import Flask, send_from_directory
from flask_cors import CORS, cross_origin
from base_api import PlayerClassStatsAPI

app = Flask(__name__, static_folder='../build',static_url_path='/')
CORS(app)  # Enable Cross-Origin Resource Sharing (CORS)
@app.route("/")
def index():
    return app.send_static_file("index.html")
# Define routes for different player classes
app.add_url_rule('/api/overall-stats',
                 view_func=PlayerClassStatsAPI.as_view('overall_stats', 'Overall Stats', 'overall_player_stats'))
app.add_url_rule('/api/demoman-stats',
                 view_func=PlayerClassStatsAPI.as_view('demoman-stats', 'Demo Stats', 'demoman_class_stats'))
app.add_url_rule('/api/soldier-stats',
                 view_func=PlayerClassStatsAPI.as_view('soldier_stats', 'Soldier Stats', 'soldier_class_stats'))
app.add_url_rule('/api/spy-stats', view_func=PlayerClassStatsAPI.as_view('spy_stats', 'Spy Stats', 'spy_class_stats'))
app.add_url_rule('/api/sniper-stats',
                 view_func=PlayerClassStatsAPI.as_view('sniper_stats', 'Sniper Stats', 'sniper_class_stats'))
app.add_url_rule('/api/medic-stats',
                 view_func=PlayerClassStatsAPI.as_view('medic_stats', 'Medic Stats', 'medic_class_stats'))
app.add_url_rule('/api/engineer-stats',
                 view_func=PlayerClassStatsAPI.as_view('engineer_stats', 'Engineer Stats', 'engineer_class_stats'))
app.add_url_rule('/api/heavyweapons-stats',
                 view_func=PlayerClassStatsAPI.as_view('heavyweapons_stats', 'Heavy Weapons Stats',
                                                       'heavyweapons_class_stats'))
app.add_url_rule('/api/scout-stats',
                 view_func=PlayerClassStatsAPI.as_view('scout_stats', 'Scout Stats', 'scout_class_stats'))
app.add_url_rule('/api/pyro-stats',
                 view_func=PlayerClassStatsAPI.as_view('pyro_stats', 'Pyro Stats', 'pyro_class_stats'))
app.add_url_rule('/api/overall-stats_30days',
                 view_func=PlayerClassStatsAPI.as_view('overall_stats_30days', 'Overall stats_30days',
                                                       'overall_player_stats_30days'))
app.add_url_rule('/api/demoman-stats_30days',
                 view_func=PlayerClassStatsAPI.as_view('demoman_stats_30days', 'Demo stats_30days',
                                                       'demoman_class_stats_30days'))
app.add_url_rule('/api/soldier-stats_30days',
                 view_func=PlayerClassStatsAPI.as_view('soldier_stats_30days', 'Soldier stats_30days',
                                                       'soldier_class_stats_30days'))
app.add_url_rule('/api/spy-stats_30days', view_func=PlayerClassStatsAPI.as_view('spy_stats_30days', 'Spy stats_30days',
                                                                                'spy_class_stats_30days'))
app.add_url_rule('/api/sniper-stats_30days',
                 view_func=PlayerClassStatsAPI.as_view('sniper_stats_30days', 'Sniper stats_30days',
                                                       'sniper_class_stats_30days'))
app.add_url_rule('/api/medic-stats_30days',
                 view_func=PlayerClassStatsAPI.as_view('medic_stats_30days', 'Medic stats_30days',
                                                       'medic_class_stats_30days'))
app.add_url_rule('/api/engineer-stats_30days',
                 view_func=PlayerClassStatsAPI.as_view('engineer_stats_30days', 'Engineer stats_30days',
                                                       'engineer_class_stats_30days'))
app.add_url_rule('/api/heavyweapons-stats_30days',
                 view_func=PlayerClassStatsAPI.as_view('heavyweapons_stats_30days', 'Heavy Weapons stats_30days',
                                                       'heavyweapons_class_stats_30days'))
app.add_url_rule('/api/scout-stats_30days',
                 view_func=PlayerClassStatsAPI.as_view('scout_stats_30days', 'Scout stats_30days',
                                                       'scout_class_stats_30days'))
app.add_url_rule('/api/pyro-stats_30days',
                 view_func=PlayerClassStatsAPI.as_view('pyro_stats_30days', 'Pyro stats_30days',
                                                       'pyro_class_stats_30days'))
if __name__ == '__main__':
    app.run()
