from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from database_info import database, secret_key
from werkzeug.utils import secure_filename
import os, subprocess, json
from flask_cors import CORS
from constants import features, labels
from user_data_utilities.user_model_data_prep import prep_user_model_data
from combo_evaluator_model import BidirectionalComboLSTM
import torch
from werkzeug.security import generate_password_hash, check_password_hash
from post_slippi_data_to_db import main


app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:3000"}})

model = BidirectionalComboLSTM()
model.load_state_dict(torch.load('model_weights.pth', map_location=torch.device('cpu')))
model.eval()

UPLOAD_FOLDER = 'player_uploads/slp_games' 
ALLOWED_EXTENSIONS = {'slp'}
temp_slippi_json_folder = 'player_uploads/user_temp_slp_data'
temp_json_data_for_d3 = 'player_uploads/d3_json_flowchart/json_data_for_frontend_visual.json'
previous_json_frontend_data = 'player_uploads/d3_json_flowchart'

csv_path_for_combo_model = 'player_uploads/combo_to_evaluate'

app.config['SECRET_KEY'] = secret_key
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

        clear_folder(previous_json_frontend_data)
        user_id = session.get('user_id')
        print('this is the user', user_id)

        try:
            subprocess.run(["node", "user_data_utilities/userSlippi.js", file_path], check=True)

            game_id = main(temp_slippi_json_folder, user_id) 

            subprocess.run(["python3", "get_combos_from_games.py", game_id], check=True)
            subprocess.run(["python3", "label_combos_for_model.py", game_id], check=True)

            with open(temp_json_data_for_d3, 'r') as file:
                d3_json_data = json.load(file)

            print('data uploaded')

            clear_folder(UPLOAD_FOLDER)
            clear_folder(temp_slippi_json_folder)

        except subprocess.CalledProcessError as e:
            return jsonify({"error": "Failed to process file"}), 500

        return jsonify(d3_json_data), 200
    else:
        return jsonify({"error": "File type not allowed"}), 400
    
@app.route('/api/score-combo', methods=['POST'])
def get_result_from_model():
    csv_data = request.data.decode('utf-8')

    os.makedirs(csv_path_for_combo_model, exist_ok=True)

    clear_folder(csv_path_for_combo_model)

    combo_csv_filename = 'user_combo_data.csv'

    combo_file_path = os.path.join(csv_path_for_combo_model, combo_csv_filename)

    with open(combo_file_path, 'w') as file:
        file.write(csv_data)

    print(f"CSV data saved to {combo_file_path}")

    input_tensor = prep_user_model_data(combo_file_path, features)

    print("Shape after unsqueeze:", input_tensor.shape)
    
    with torch.no_grad():
        prediction = model(input_tensor)
    
    prediction_list = prediction.tolist()
    
    if len(prediction_list) == 1:
        prediction_list = prediction_list[0]

    score_pairs = {label: score for label, score in zip(labels, prediction_list)}

    return jsonify(score_pairs), 200

@app.route('/register', methods=['POST'])
def register():
    from sql_models import User  # Local import

    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password') 

    # Check if user already exists
    existing_user = combo_db.session.query(User).filter_by(username=username).first()
    if existing_user:
        return jsonify({"message": "Username already taken"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password_hash=hashed_password)

    combo_db.session.add(new_user)
    combo_db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    from sql_models import User  # Local import of User

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = combo_db.session.query(User).filter_by(username=username).first()

    if user and user.check_password(password):
        session['user_id'] = user.id
        print(f"User ID set in session: {session['user_id']}")  # Print statement to verify
        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
        return jsonify({"message": "Login successful", "user": user_data}), 200

    return jsonify({"message": "Invalid username or password"}), 401


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None) 
    return jsonify({"message": "Logged out"}), 200


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
