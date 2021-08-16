from scraping_script import DATABASE_NAME
DELIMITER = ";"
# consult headers when writing data to have correct order
GAME_INFO_HEADERS = ["game_date", "game_time", "game_url", "sport_type", "home_team", "away_team",
                     "home_score", "away_score", "full_scoreline", "odds_type", "avg_home_odds", "avg_away_odds", "highest_home_odds", "highest_away_odds", "time_scraped"]

BETTING_INFO_HEADERS = ["game_date", "game_time", "game_url", "sport_type", "home_team", "away_team", "bookie", "odds_type", "home_odds", "away_odds", "time_scraped"]

import time
import pprint
import os
import sys
from datetime import datetime
import json
import csv
import sqlite3


## connect
db_conn = sqlite3.connect(DATABASE_NAME)
db_cursor = db_conn.cursor()

## create csv files
base_outputname = datetime.now().strftime("%m-%d-%Y %H_%M_%S")
game_info_filename = base_outputname + " game_info.csv"
betting_info_filename = base_outputname + " betting_info.csv"
game_info_file = open(game_info_filename, 'w', newline='', encoding='utf-8')
game_info_writer = csv.writer(game_info_file, delimiter=DELIMITER, quoting=csv.QUOTE_MINIMAL)
betting_info_file = open(betting_info_filename, 'w', newline='', encoding='utf-8')
betting_info_writer = csv.writer(betting_info_file, delimiter=DELIMITER, quoting=csv.QUOTE_MINIMAL)
# write headers
ccc = game_info_writer.writerow(GAME_INFO_HEADERS)
ccc = betting_info_writer.writerow(BETTING_INFO_HEADERS)



## select all games sorted by time of playing, write them to 2 files!
for game in db_cursor.execute("SELECT * FROM GamesTable ORDER BY date_unix DESC"):
    if game[9] == None:
        print("No odds data scraped for game", game[0])
        continue
    
    odds_json = json.loads(game[9])
    # write data to both files - first for game info file
    ccc = game_info_writer.writerow([game[5], game[6], game[0], odds_json["sport"], game[1], game[2], game[3], game[4], game[8], odds_json["odds_type"],
                                     odds_json["average_home"], odds_json["average_away"], odds_json["highest_home"], odds_json["highest_away"], odds_json["time_of_scraping"]])

    # write into betting info file
    for odds_item in odds_json["odds"]:
        ccc = betting_info_writer.writerow([game[5], game[6], game[0], odds_json["sport"], game[1], game[2], odds_item["bookie"], odds_json["odds_type"], odds_item["home"], odds_item["away"], odds_json["time_of_scraping"]])
        
    
    
    
## end of program
game_info_file.close()
betting_info_file.close()
print("Created file with game info:", game_info_filename)
print("Created file with betting info:", betting_info_filename)
db_cursor.close()
db_conn.close()
