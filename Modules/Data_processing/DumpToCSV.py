import csv
import mysql.connector
import os


def export_table_to_csv(cursor, table_name, filename):
    select_query = f"SELECT * FROM {table_name}"
    cursor.execute(select_query)
    rows = cursor.fetchall()

    with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([i[0] for i in cursor.description])  # Write column headers
        csv_writer.writerows(rows)

def main():
    # Connect to MySQL database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="highlanderpugs"
    )
    mycursor = mydb.cursor()

    # List of table names to export
    table_names = ['player_stats',"Overall_player_stats_30days",'overall_player_stats', 'scout_class_stats_30days', 'soldier_class_stats_30days', 'demoman_class_stats_30days', 'medic_class_stats_30days', 'sniper_class_stats_30days', 'heavyweapons_class_stats_30days', 'pyro_class_stats_30days', 'spy_class_stats_30days', 'engineer_class_stats_30days',"Overall_player_stats",'overall_player_stats', 'scout_class_stats', 'soldier_class_stats', 'demoman_class_stats', 'medic_class_stats', 'sniper_class_stats', 'heavyweapons_class_stats', 'pyro_class_stats', 'spy_class_stats', 'engineer_class_stats']

    # Create a directory if it doesn't exist
    if not os.path.exists('../../CSV'):
        os.makedirs('../../CSV')

    # Export data for each table to CSV files
    for table_name in table_names:
        filename = os.path.join('../../CSV', f'{table_name}.csv')
        export_table_to_csv(mycursor, table_name, filename)
        print(f'Exported {table_name} to {filename}')

    # Close the database connection
    mydb.close()

if __name__ == "__main__":
    main()


