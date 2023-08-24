import mysql.connector

def calculate_overall_stats(player_stats_list):
    overall_stats = {
        "kills": 0,
        "assists": 0,
        "deaths": 0,
        "dmg": 0,
        "wins": 0,
        "matches_played": len(player_stats_list),
        "win_rate": 0,  # Initialize win rate to 0
        "total_time_played": 0,  # Initialize total time played to 0
        "dapm": 0  # Initialize DAPM to 0
    }

    for player_stats in player_stats_list:
        overall_stats["kills"] += player_stats["kills"]
        overall_stats["assists"] += player_stats["assists"]
        overall_stats["deaths"] += player_stats["deaths"]
        overall_stats["dmg"] += player_stats["dmg"]
        overall_stats["total_time_played"] += player_stats["total_time"]
        # Access the correct nested value for "winner"
        winner_value = int(player_stats["winner"])
        overall_stats["wins"] += winner_value

    # Calculate win rate
    if overall_stats["matches_played"] > 0:
        overall_stats["win_rate"] = (overall_stats["wins"] / overall_stats["matches_played"]) * 100

    # Calculate DAPM (Damage Per Minute)
    if overall_stats["total_time_played"] > 0:
        overall_stats["dapm"] = (overall_stats["dmg"] / overall_stats["total_time_played"]) * 60

    return overall_stats

def main():
    # Connect to MySQL database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="highlanderpugs"
    )
    mycursor = mydb.cursor()

    # Create overall_player_stats table if not exists
    create_overall_stats_table_sql = """
    CREATE TABLE IF NOT EXISTS overall_player_stats (
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
        dapm DECIMAL(10, 2)  -- Add DAPM as a DECIMAL type with 10 total digits and 2 decimal places
    )
    """
    mycursor.execute(create_overall_stats_table_sql)

    truncate_sql = f"TRUNCATE TABLE overall_player_stats"
    mycursor.execute(truncate_sql)
    mydb.commit()

    # Get distinct steam IDs from the database
    mycursor.execute("SELECT DISTINCT steamid FROM player_stats")
    steam_ids = mycursor.fetchall()

    for steam_id in steam_ids:
        steam_id = steam_id[0]
        # Fetch the ETF2L name for the steam ID
        mycursor.execute("SELECT etf2l_name FROM player_stats WHERE steamid = %s LIMIT 1", (steam_id,))
        etf2l_name = mycursor.fetchone()[0]

        # Fetch all rows tied to the steam ID
        mycursor.execute("SELECT * FROM player_stats WHERE steamid = %s", (steam_id,))
        rows = mycursor.fetchall()

        player_stats_list = []
        for row in rows:
            player_stats = {
                "Etf2l_Name": row[3],
                "kills": row[5],
                "assists": row[6],
                "deaths": row[7],
                "dmg": row[8],
                "dapm": row[11],
                "winner": row[10],
                "total_time": row[14]  # Include total time played in player stats
            }
            player_stats_list.append(player_stats)

        overall_stats = calculate_overall_stats(player_stats_list)

        # Insert or update overall stats for the steam ID and ETF2L name in the new table
        upsert_sql = """
        INSERT INTO overall_player_stats (steamid, etf2l_name, overall_kills, overall_assists, overall_deaths, overall_dmg, overall_wins, matches_played, win_rate, dapm)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        etf2l_name = %s, overall_kills = %s, overall_assists = %s, overall_deaths = %s, overall_dmg = %s, overall_wins = %s, matches_played = %s, win_rate = %s, dapm = %s
        """
        val = (steam_id, etf2l_name, overall_stats["kills"], overall_stats["assists"],
               overall_stats["deaths"], overall_stats["dmg"], overall_stats["wins"], overall_stats["matches_played"],
               overall_stats["win_rate"],overall_stats["dapm"],
               etf2l_name, overall_stats["kills"], overall_stats["assists"],
               overall_stats["deaths"], overall_stats["dmg"], overall_stats["wins"], overall_stats["matches_played"],
               overall_stats["win_rate"], overall_stats["dapm"])
        mycursor.execute(upsert_sql, val)
        mydb.commit()

    # Close the database connection
    mydb.close()

if __name__ == "__main__":
    main()
