import mysql.connector

def calculate_overall_class_stats(player_stats_list):
    overall_class_stats = {
        "kills": 0,
        "assists": 0,
        "deaths": 0,
        "dmg": 0,
        "wins": 0,
        "matches_played": len(player_stats_list),
        "win_rate": 0,
        "dapm": 0  # Initialize DAPM to 0
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

        # Sum up DAPM values for each match
        overall_class_stats["dapm"] += float(player_stats.get("dapm", 0))

    # Calculate win rate
    if overall_class_stats["matches_played"] > 0:
        overall_class_stats["win_rate"] = (overall_class_stats["wins"] / overall_class_stats["matches_played"]) * 100

    # Calculate average DAPM per match
        if total_time_minutes> 0:
            overall_class_stats["dapm"] = (overall_class_stats["dmg"] / total_time_minutes )

    return overall_class_stats

def main():
    # Connect to MySQL database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Add your MySQL password here
        database="highlanderpugs"
    )
    mycursor = mydb.cursor()

    # Fetch distinct Steam IDs and ETF2L names from the player_stats table
    mycursor.execute("SELECT DISTINCT steamid, etf2l_name FROM player_stats")
    steam_ids_and_names = mycursor.fetchall()

    # List of player classes
    player_classes = ["soldier", "pyro", "demoman", "heavyweapons", "engineer", "medic", "sniper", "spy", "scout"]
    for player_class in player_classes:
        truncate_sql = f"TRUNCATE TABLE {player_class.lower()}_class_stats"
        mycursor.execute(truncate_sql)
    for steam_id_name_tuple in steam_ids_and_names:
        steam_id = steam_id_name_tuple[0]  # Extract the Steam ID
        etf2l_name = steam_id_name_tuple[1]  # Extract the ETF2L name

        for player_class in player_classes:
            # Check if there are any rows for the given Steam ID and class in the player_stats table
            mycursor.execute("SELECT COUNT(*) FROM player_stats WHERE steamid = %s AND player_class = %s", (steam_id, player_class))
            row_count = mycursor.fetchone()[0]

            if row_count == 0:
                continue  # Skip if no rows are found

            # Fetch all rows tied to the Steam ID and player class
            mycursor.execute("SELECT * FROM player_stats WHERE steamid = %s AND player_class = %s", (steam_id, player_class))
            rows = mycursor.fetchall()

            class_stats_list = []
            for row in rows:
                class_stats = {
                    "Etf2l_Name": row[3],
                    "kills": row[5],
                    "assists": row[6],
                    "deaths": row[7],
                    "dmg": row[8],
                    "dapm": row[11],
                    "winner": row[10],
                    "total_time": row[14] # Assuming you have a "dapm" field in your player_stats data
                }
                class_stats_list.append(class_stats)

            overall_class_stats = calculate_overall_class_stats(class_stats_list)

            # Create a new table for the player class if not exists
            create_class_stats_table_sql = f"""
            CREATE TABLE IF NOT EXISTS {player_class.lower()}_class_stats (
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
                dapm DECIMAL(10, 2)  # Add DAPM as a DECIMAL type with 10 total digits and 2 decimal places
            )
            """
            mycursor.execute(create_class_stats_table_sql)

            # Insert or update overall stats for the player class and Steam ID in the new table
            upsert_sql = f"""
            INSERT INTO {player_class.lower()}_class_stats (steamid, etf2l_name, overall_kills, overall_assists, overall_deaths, overall_dmg, overall_wins, matches_played, win_rate, dapm)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            etf2l_name = %s, overall_kills = %s, overall_assists = %s, overall_deaths = %s, overall_dmg = %s, overall_wins = %s, matches_played = %s, win_rate = %s, dapm = %s
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
                overall_class_stats["win_rate"],  # Include win rate in the values
                overall_class_stats["dapm"], # Include DAPM in the values
                etf2l_name,
                overall_class_stats["kills"],
                overall_class_stats["assists"],
                overall_class_stats["deaths"],
                overall_class_stats["dmg"],
                overall_class_stats["wins"],
                overall_class_stats["matches_played"],
                overall_class_stats["win_rate"],  # Include win rate in the update values
                overall_class_stats["dapm"]  # Include DAPM in the update values
            )
            mycursor.execute(upsert_sql, val)
            mydb.commit()

    # Close the database connection
    mydb.close()

if __name__ == "__main__":
    main()
