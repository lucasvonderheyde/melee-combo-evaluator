import pandas as pd
from database_info import database, game_id, combo_table_select, combo_table_columns_to_post_to
from constants import stage_ids
import psycopg2

def move_combo_data_to_proper_stage():
    
    connection = psycopg2.connect(database)

    cursor = connection.cursor()

    cursor.execute(f"SELECT stage_id FROM settings WHERE game_id = %s", [game_id])
    stage_id = cursor.fetchone()[0]

    print(game_id)
    
    if cursor.rowcount == 0:
        raise ValueError("No data found to insert. Aborting operation.")

    combo_table = None
    for key, value in stage_ids.items():
        if key == stage_id:
            combo_table = f"combos_for_{value}"
            break

    if combo_table:
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {combo_table} AS 
                {combo_table_select}    
            ''', [game_id])
        
    cursor.execute(f'''INSERT INTO {combo_table} {combo_table_columns_to_post_to}
            {combo_table_select}''', [game_id])
    
    connection.commit()

    cursor.close()
    connection.close()
    
move_combo_data_to_proper_stage()
