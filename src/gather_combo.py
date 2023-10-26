import pandas as pd
from sqlalchemy import create_engine
from database_info import database

engine = create_engine(database)



pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', 60)

query = "SELECT * FROM higher_port_player_post_frames LEFT JOIN higher_port_player_pre_frames ON higher_port_player_post_frames.frame = higher_port_player_pre_frames.frame"

dataframe = pd.read_sql(query, engine)

print(dataframe)
