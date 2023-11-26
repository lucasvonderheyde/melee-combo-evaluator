import pandas as pd
from database_info import database, game_id, combo_table_generator
from constants import stage_ids
import psycopg2


def generate_stage_table_for_database():
    
    connection = psycopg2.connect(database)

    cursor = connection.cursor()

    cursor.execute(f"SELECT stage_id FROM settings WHERE game_id = %s", [game_id])
    stage_id = cursor.fetchone()[0]

    combo_table = None
    for key, value in stage_ids.items():
        if key == stage_id:
            combo_table = f"combos_for_{value}"
            break

    if cursor.rowcount == 0:
        raise ValueError("No data found to insert. Aborting operation.")

    cursor.execute(f'''CREATE TABLE {combo_table} AS SELECT {combo_table_generator} ''', [game_id])

    connection.commit()

    cursor.close()
    connection.close()


def generate_generic_combo_table(game_id):
    
    connection = psycopg2.connect(database)
    cursor = connection.cursor()

    # This creates a general combos table
    combo_table = "combos"

    # Using the game_id in the SQL query  # Make sure combo_table_generator is designed to accept a game_id parameter

    cursor.execute(f"CREATE TABLE IF NOT EXISTS {combo_table} AS SELECT {combo_table_generator}", [game_id])

    connection.commit()

    cursor.close()
    connection.close()

generate_generic_combo_table(game_id)

