from flask import jsonify, request
from flask.views import MethodView
import mysql.connector
def create_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',  # Add your MySQL password here
        database='highlanderpugs'
    )

class PlayerClassStatsAPI(MethodView):
    def __init__(self, class_name, table_name):
        self.class_name = class_name
        self.table_name = table_name

    def get(self):
        try:
            connection = create_db_connection()
            cursor = connection.cursor()

            page = request.args.get('page', default=1, type=int)
            per_page = 1000
            search = request.args.get('search', '')
            start_index = (page - 1) * per_page

            # Construct the SQL query with or without search functionality
            if search:
                query = (
                    f"SELECT steamid, etf2l_name, overall_kills, overall_assists, "
                    f"overall_deaths, overall_dmg, overall_wins, dapm, matches_played, win_rate "
                    f"FROM {self.table_name} "
                    f"WHERE etf2l_name LIKE %s "
                    f"LIMIT %s OFFSET %s"
                )

                # Execute the query with the search query parameter
                cursor.execute(query, (f"%{search}%", per_page, start_index))
            else:
                query = (
                    f"SELECT steamid, etf2l_name, overall_kills, overall_assists, "
                    f"overall_deaths, overall_dmg, overall_wins, dapm, matches_played, win_rate "
                    f"FROM {self.table_name} "
                    f"LIMIT %s OFFSET %s"
                )

                # Execute the query without a search query
                cursor.execute(query, (per_page, start_index))

            # Fetch the results
            rows = cursor.fetchall()

            if rows:
                # Convert the results to a list of dictionaries
                stats = []
                for row in rows:
                    data = {
                        'steamid': row[0],
                        'etf2l_name': row[1],
                        'overall_kills': row[2],
                        'overall_assists': row[3],
                        'overall_deaths': row[4],
                        'overall_dmg': row[5],
                        'dapm': row[6],  # Corrected dapm index
                        'overall_wins': row[7],
                        'matches_played': row[8],
                        'win_rate': float(row[9])  # Convert win_rate to a float
                    }
                    stats.append(data)

                return jsonify(stats)
            else:
                return jsonify({'message': 'No data found'}), 404

        except Exception as e:
            return jsonify({'error': str(e)}), 500

        finally:
            cursor.close()
            connection.close()