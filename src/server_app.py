from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from database_info import database
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS
from sql_models import Metadata, GameInfo, MatchInfo, PlayersInfo, Settings, HigherPortPlayerPostFrames, LowerPortPlayerPostFrames, HigherPortPlayerPreFrames, LowerPortPlayerPreFrames

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'player_uploads/slp_games' 
ALLOWED_EXTENSIONS = {'slp'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
combo_db = SQLAlchemy(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return '<h1>test the flask server</h1>', 200

@app.route('/players-uploads', methods=['POST'])
def upload_file():
    if 'slpFile' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['slpFile']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return jsonify({"message": "File successfully uploaded"}), 200
    else:
        return jsonify({"error": "File type not allowed"}), 400



if __name__ == "__main__":
    app.run()