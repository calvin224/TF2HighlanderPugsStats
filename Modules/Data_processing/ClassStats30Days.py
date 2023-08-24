import mysql.connector
from datetime import datetime, timedelta

def calculate_overall_class_stats(player_stats_list):
    overall_class_stats = {
        "kills": 0,
        "assists": 0,
        "deaths": 0,
        "dmg": 0,
        "wins": 0,
        "matches_played": len(player_stats_list),
        "win_rate": 0,
        "dapm": 0,  # Initialize DAPM to 0
    }

    total_time_minutes = 0  # Initialize total time in minutes to calculate average DAPM

    for player_stats in player_stats_list:
        overall_class_stats["kills"] += player_stats["kills"]
        overall_class_stats["assists"] += player_stats["assists"]
        overall_class_stats["deaths"] += player_stats["deaths"]
        overall_class_stats["dmg"] += player_stats["dmg"]

        winner_value = int(player_stats["winner"])
        overall_class_stats["wins"] += winner_value

        # Assuming you have a "total_time" field in your player_stats data (in seconds)
        total_time_minutes += player_stats.get("total_time", 0) / 60  # Convert seconds to minutes

        # Assuming you have a "total_time" field in your player_stats data (in seconds)
        total_time_minutes += player_stats.get("total_time", 0) / 60  # Convert seconds to minutes

        # Sum up DAPM values for each match
        overall_class_stats["dapm"] += float(player_stats.get("dapm", 0))

    # Calculate win rate
    if overall_class_stats["matches_played"] > 0:
        overall_class_stats["win_rate"] = (overall_class_stats["wins"] / overall_class_stats["matches_played"]) * 100

    # Calculate average DAPM per match
    if total_time_minutes > 0:
        overall_class_stats["dapm"] = (overall_class_stats["dapm"] / total_time_minutes*60)

    return overall_class_stats

def main():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="highlanderpugs"
    )
    mycursor = mydb.cursor()

    thirty_days_ago_unix = int((datetime.now() - timedelta(days=30)).timestamp())
    thirty_days_ago_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

    print(f"Retrieving data for the last 30 days from {thirty_days_ago_date} to today.")

    # List of player classes
    player_classes = ["soldier", "pyro", "demoman", "heavyweapons", "engineer", "medic", "sniper", "spy", "scout"]

    for player_class in player_classes:
        # Create a temporary table for the current class and the last 30 days
        create_temp_table_sql = f"""
        CREATE TEMPORARY TABLE temp_{player_class.lower()}_class_stats AS
        SELECT *, FROM_UNIXTIME(date) as converted_date FROM player_stats
        WHERE date >= {thirty_days_ago_unix} AND player_class = "{player_class}"
        """
        mycursor.execute(create_temp_table_sql)

        # Fetch distinct Steam IDs and ETF2L names for the current class
        mycursor.execute(f"SELECT DISTINCT steamid, etf2l_name FROM temp_{player_class.lower()}_class_stats")
        steam_ids_and_names = mycursor.fetchall()

        for steam_id_name_tuple in steam_ids_and_names:
            steam_id = steam_id_name_tuple[0]
            etf2l_name = steam_id_name_tuple[1]

            # Fetch all rows tied to the Steam ID and class
            mycursor.execute(f"SELECT * FROM temp_{player_class.lower()}_class_stats WHERE steamid = %s", (steam_id,))
            rows = mycursor.fetchall()

            class_stats_list = []
            for row in rows:
                class_stats = {
                    "kills": row[5],
                    "assists": row[6],
                    "deaths": row[7],
                    "dmg": row[8],
                    "winner": row[10],
                    "dapm": row[11],
                    "total_time": row[14]  # Assuming you have a "total_time" field in your player_stats data
                }
                class_stats_list.append(class_stats)

            overall_class_stats = calculate_overall_class_stats(class_stats_list)

            # Create a new table for the player class if not exists
            create_class_stats_table_sql = f"""
            CREATE TABLE IF NOT EXISTS {player_class.lower()}_class_stats_30days (
                id INT AUTO_INCREMENT PRIMARY KEY,
                steamid VARCHAR(255),
                etf2l_name VARCHAR(255),
                overall_kills INT,
                overall_assists INT,
                overall_deaths INT,
                overall_dmg INT,
                overall_wins INT,
                matches_played INT,
                win_rate DECIMAL(5, 2),
                dapm DECIMAL(10, 2),
                date_played DATE
            )
            """
            mycursor.execute(create_class_stats_table_sql)

            # Insert or update overall stats for the player class and Steam ID in the new table
            upsert_sql = f"""
            INSERT INTO {player_class.lower()}_class_stats_30days (steamid, etf2l_name, overall_kills, overall_assists, overall_deaths, overall_dmg, overall_wins, matches_played, win_rate, dapm, date_played)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            etf2l_name = %s, overall_kills = %s, overall_assists = %s, overall_deaths = %s, overall_dmg = %s, overall_wins = %s, matches_played = %s, win_rate = %s, dapm = %s, date_played = %s
            """
            val = (
                steam_id,
                etf2l_name,
                overall_class_stats["kills"],
                overall_class_stats["assists"],
                overall_class_stats["deaths"],
                overall_class_stats["dmg"],
                overall_class_stats["wins"],
                overall_class_stats["matches_played"],
                overall_class_stats["win_rate"],
                overall_class_stats["dapm"],
                thirty_days_ago_date,  # Include the date played
                etf2l_name,
                overall_class_stats["kills"],
                overall_class_stats["assists"],
                overall_class_stats["deaths"],
                overall_class_stats["dmg"],
                overall_class_stats["wins"],
                overall_class_stats["matches_played"],
                overall_class_stats["win_rate"],
                overall_class_stats["dapm"],
                thirty_days_ago_date  # Include the date played in the update values
            )
            mycursor.execute(upsert_sql, val)
            mydb.commit()

    # Close the database connection
    mydb.close()

if __name__ == "__main__":
    main()
