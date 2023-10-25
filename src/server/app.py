from flask import Flask, make_response
from flask_sqlalchemy import SQLAlchemy
from database_info import database

from models import Metadata, GameInfo, MatchInfo, PlayersInfo, Settings, HigherPortPlayerPostFrames, LowerPortPlayerPostFrames, HigherPortPlayerPreFrames, LowerPortPlayerPreFrames
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = database
app.cofig['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

combo_db = SQLAlchemy(app)

@app.route("/combos")
def query_combos():
    pass

if __name__ == "__main__":
    app.run()