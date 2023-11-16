from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from database_info import database
from werkzeug.utils import secure_filename
import os, subprocess, json
from flask_cors import CORS
from sql_models import Metadata, GameInfo, MatchInfo, PlayersInfo, Settings, HigherPortPlayerPostFrames, LowerPortPlayerPostFrames, HigherPortPlayerPreFrames, LowerPortPlayerPreFrames



app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'player_uploads/slp_games' 
ALLOWED_EXTENSIONS = {'slp'}
temp_slippi_json_folder = 'player_uploads/user_temp_slp_data'
temp_json_data_for_d3 = 'player_uploads/d3_json_flowchart/json_data_for_frontend_visual.json'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
os.environ['CALLED_FROM_FLASK'] = '1'

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

        try:
            subprocess.run(["node", "user_data_utilities/userSlippi.js", file_path], check=True)

            result = subprocess.run(["python3", '-u', "post_slippi_data_to_db.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)  
            game_id = result.stdout.strip()

            subprocess.run(["python3", "get_combos_from_games.py", game_id], check=True)
            subprocess.run(["python3", "label_combos_for_model.py", game_id], check=True)

            with open(temp_json_data_for_d3, 'r') as file:
                d3_json_data = json.load(file)

            print('data uploaded')

            clear_folder(UPLOAD_FOLDER)
            clear_folder(temp_slippi_json_folder)

        except subprocess.CalledProcessError as e:
            return jsonify({"error": "Failed to process file"}), 500

        return d3_json_data, 200
    else:
        return jsonify({"error": "File type not allowed"}), 400

def clear_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

if __name__ == "__main__":
    app.run()
