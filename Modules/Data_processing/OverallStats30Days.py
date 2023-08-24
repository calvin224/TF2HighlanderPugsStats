import mysql.connector
from datetime import datetime, timedelta

def calculate_overall_stats(player_stats_list):
    overall_stats = {
        "kills": 0,
        "assists": 0,
        "deaths": 0,
        "dmg": 0,
        "wins": 0,
        "matches_played": len(player_stats_list),
        "win_rate": 0,
        "total_time_played": 0,
        "dapm": 0
    }

    for player_stats in player_stats_list:
        overall_stats["kills"] += player_stats["kills"]
        overall_stats["assists"] += player_stats["assists"]
        overall_stats["deaths"] += player_stats["deaths"]
        overall_stats["dmg"] += player_stats["dmg"]
        overall_stats["total_time_played"] += player_stats["total_time"]
        winner_value = int(player_stats["winner"])
        overall_stats["wins"] += winner_value

    if overall_stats["matches_played"] > 0:
        overall_stats["win_rate"] = (overall_stats["wins"] / overall_stats["matches_played"]) * 100

    if overall_stats["total_time_played"] > 0:
        overall_stats["dapm"] = (overall_stats["dmg"] / overall_stats["total_time_played"]) * 60

    return overall_stats

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

    create_temp_table_sql = f"""
    CREATE TEMPORARY TABLE temp_player_stats AS
    SELECT *, FROM_UNIXTIME(date) as converted_date FROM player_stats
    WHERE date >= {thirty_days_ago_unix}
    """
    mycursor.execute(create_temp_table_sql)

    create_overall_stats_table_sql = """
    CREATE TABLE IF NOT EXISTS overall_player_stats_30days (
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
    mycursor.execute(create_overall_stats_table_sql)

    truncate_sql = f"TRUNCATE TABLE overall_player_stats_30days"
    mycursor.execute(truncate_sql)
    mydb.commit()

    mycursor.execute("SELECT DISTINCT steamid FROM temp_player_stats")
    steam_ids = mycursor.fetchall()

    for steam_id in steam_ids:
        steam_id = steam_id[0]
        mycursor.execute("SELECT etf2l_name FROM temp_player_stats WHERE steamid = %s LIMIT 1", (steam_id,))
        etf2l_name = mycursor.fetchone()[0]

        mycursor.execute("SELECT * FROM temp_player_stats WHERE steamid = %s", (steam_id,))
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
                "total_time": row[14],
                "date_played": row[15].strftime('%Y-%m-%d')
            }
            player_stats_list.append(player_stats)

        overall_stats = calculate_overall_stats(player_stats_list)

        overall_stats["date_played"] = thirty_days_ago_date

        upsert_sql = """
        INSERT INTO overall_player_stats_30days (steamid, etf2l_name, overall_kills, overall_assists, overall_deaths, overall_dmg, overall_wins, matches_played, win_rate, dapm, date_played)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        etf2l_name = %s, overall_kills = %s, overall_assists = %s, overall_deaths = %s, overall_dmg = %s, overall_wins = %s, matches_played = %s, win_rate = %s, dapm = %s, date_played = %s
        """
        val = (steam_id, etf2l_name, overall_stats["kills"], overall_stats["assists"],
               overall_stats["deaths"], overall_stats["dmg"], overall_stats["wins"], overall_stats["matches_played"],
               overall_stats["win_rate"], overall_stats["dapm"], overall_stats["date_played"],
               etf2l_name, overall_stats["kills"], overall_stats["assists"],
               overall_stats["deaths"], overall_stats["dmg"], overall_stats["wins"], overall_stats["matches_played"],
               overall_stats["win_rate"], overall_stats["dapm"], overall_stats["date_played"])
        mycursor.execute(upsert_sql, val)
        mydb.commit()

    mydb.close()

if __name__ == "__main__":
    main()
