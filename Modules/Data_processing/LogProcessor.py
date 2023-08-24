import mysql.connector
import requests
import time
import json

MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds


def get_etf2l_name(steam_id):
    url = f"https://api.etf2l.org/player/{steam_id}.json"
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            etf2l_name = data.get('player', {}).get('name')
            return etf2l_name
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            print(f"Error fetching ETF2L name for Steam ID: {steam_id}. Retrying in {RETRY_DELAY} seconds...")
            retries += 1
            time.sleep(RETRY_DELAY)

    print(f"Failed to fetch ETF2L name for Steam ID: {steam_id} after {MAX_RETRIES} retries.")
    return ""


def writetodb(data, mycursor, mydb, log_date, log_title):
    create_table_sql = """
        CREATE TABLE IF NOT EXISTS player_stats (
            id INT AUTO_INCREMENT PRIMARY KEY,
            steamid VARCHAR(255),
            etf2l_name VARCHAR(255),
            team VARCHAR(255),
            player_class VARCHAR(255),
            kills INT,
            assists INT,
            deaths INT,
            dmg INT,
            weapon VARCHAR(255),
            winner INT,
            dapm FLOAT,
            date VARCHAR(255),
            title VARCHAR(255),
            total_time INT  -- Add total_time column
        )
    """

    mycursor.execute(create_table_sql)

    date = log_date
    title = log_title

    for steam_id, player_data in data['players'].items():
        team = player_data['team']
        etf2l_name = get_etf2l_name(steam_id)

        for class_stat in player_data['class_stats']:
            player_class = class_stat['type']
            kills = class_stat['kills']
            assists = class_stat['assists']
            deaths = class_stat['deaths']
            dmg = class_stat['dmg']
            weapon = class_stat['weapon']
            total_time = class_stat['total_time']

            if total_time > 0:
                dapm = (dmg / total_time) * 60  # DPM = (Total Damage / Total Time) * 60
            else:
                dapm = 0.0

            rounds = data.get('rounds', [])
            for round_info in rounds:
                winner = round_info.get('winner')
                if winner == team:
                    winner_value = 1
                else:
                    winner_value = 0

            steam_id_value = steam_id
            team = str(team)
            player_class = str(player_class)
            kills = int(kills)
            assists = int(assists)
            deaths = int(deaths)
            dmg = int(dmg)
            weapon = str(weapon)

            max_weapon_length = 255
            if len(weapon) > max_weapon_length:
                weapon = weapon[:max_weapon_length]

            check_row_sql = """
                SELECT COUNT(*) FROM player_stats
                WHERE steamid = %s AND team = %s AND player_class = %s AND kills = %s
                AND assists = %s AND deaths = %s AND dmg = %s AND winner = %s
            """

            check_val = (
                steam_id_value, team, player_class, kills, assists, deaths, dmg, winner_value
            )

            mycursor.execute(check_row_sql, check_val)
            row_exists = mycursor.fetchone()[0] > 0

            if row_exists is False:
                insert_sql = """
                    INSERT INTO player_stats (steamid, etf2l_name, team, player_class, kills, assists, deaths, dmg, weapon, winner, dapm, date, title, total_time)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

                val = (
                    steam_id_value, etf2l_name, team, player_class, kills, assists, deaths, dmg, weapon, winner_value,
                    dapm, date, title, total_time
                )
                mycursor.execute(insert_sql, val)
                mydb.commit()


def get_log_data(log_id):
    url = f"https://logs.tf/api/v1/log/{log_id}"
    response = requests.get(url)
    if response.status_code == 429:
        print(f"Log {log_id} not found. Moving to the next log.")
        return None
    if response.status_code != 200:
        print(f"Log {log_id} not found. Moving to the next log.")
        return None
    data = json.loads(response.content)
    return data


def main():
    mydb = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",
        database="highlanderpugs"
    )
    mycursor = mydb.cursor()

    title_prefix = "hl.tf2pickup.eu"
    limit = 10000
    offset = 0
    processed_logs = set()

    while True:
        url = f"http://logs.tf/api/v1/log?title={title_prefix}&limit={limit}"
        response = requests.get(url)
        print(url)

        if response.status_code != 200:
            print(f"Error fetching logs. Exiting.")

        data = json.loads(response.content)

        if not data["logs"]:
            print("No more logs found. Exiting.")
            break

        for log in data["logs"]:
            log_id = log["id"]
            log_title = log["title"]
            log_date = log["date"]
            log_key = f"{log_title}"

            if log_key in processed_logs:
                print(f"Skipping duplicate log: {log_title}")
                continue

            processed_logs.add(log_key)
            print(f"Found log: {log_title}")

            log_data = get_log_data(log_id)
            if log_data is not None:
                writetodb(log_data, mycursor, mydb, log_date, log_title)

        offset += len(data["logs"])
        time.sleep(5)

    mydb.close()


if __name__ == "__main__":
    main()
