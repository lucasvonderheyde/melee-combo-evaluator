import pandas as pd
import psycopg2
from database_info import database, game_id

connection = psycopg2.connect(database)

cursor = connection.cursor()

get_combos_from_game = ("SELECT stage_id FROM combos_for_battlefield WHERE game_id = %s", [game_id])

df = pd.read_sql_query(get_combos_from_game, connection)


print(df)