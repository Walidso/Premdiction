from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Match, Prediction
import requests
from flask_swagger_ui import get_swaggerui_blueprint
from dotenv import load_dotenv
import os

app = Flask(__name__)                                #change the absolute path for the database file here
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\walid\\Desktop\\Service Design\\Premdiction\\instance\\database.db'
db.init_app(app)
API_KEY = os.getenv('API_KEY')
with app.app_context():
    db.create_all()
load_dotenv()
# Instructions for flask-swagger-ui
SWAGGER_URL = "/api/docs"  # Where should the user go to read these docs
API_URL = "/static/premdiction.yaml"  # Which file should be used to generate the docs

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "premdiction_API"
    }
)

app.register_blueprint(swaggerui_blueprint)


@app.route('/')
def home():
    return "PREMDIKTION your premier league prediction app"


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Bad request'}), 400
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'New user registered'})


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Bad request'}), 400
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Login failed'}), 401
    return jsonify({'message': 'Logged in successfully'})


@app.route('/predictions', methods=['POST'])
def create_prediction():
    data = request.get_json()
    if not data or 'user_id' not in data or 'match_id' not in data or 'result' not in data:
        return jsonify({'message': 'Bad request'}), 400
    if data['result'] not in ['1', 'X', '2']:
        return jsonify({'message': 'Invalid result. Must be "1", "X", or "2"'})
    new_prediction = Prediction(user_id=data['user_id'], match_id=data['match_id'], result=data['result'])
    db.session.add(new_prediction)
    db.session.commit()
    return jsonify({'message': 'Prediction created'})


@app.route('/matches/<id>', methods=['PUT'])
def update_match(id):
    data = request.get_json()
    if not data or 'result' not in data:
        return jsonify({'message': 'Bad request'}), 400
    match = Match.query.get(id)
    if not match:
        return jsonify({'message': 'Match not found'})
    match.result = data['result']
    db.session.commit()
    predictions = Prediction.query.filter_by(match_id=id).all()
    for prediction in predictions:
        if prediction.result == match.result:
            user = User.query.get(prediction.user_id)
            user.score += 1
            db.session.commit()
    return jsonify({'message': 'Match and scores updated'})


@app.route('/users/high_scores', methods=['GET'])
def get_high_scores():
    users = User.query.order_by(User.score.desc()).all()
    output = []
    for user in users:
        user_data = {}
        user_data['username'] = user.username
        user_data['score'] = user.score
        output.append(user_data)
    return jsonify({'users': output})


@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'})
    user_data = {}
    user_data['username'] = user.username
    user_data['score'] = user.score
    return jsonify({'user': user_data})


@app.route('/predictions', methods=['GET'])
def get_predictions():
    predictions = Prediction.query.all()
    output = []
    for prediction in predictions:
        prediction_data = {}
        prediction_data['user_id'] = prediction.user_id
        prediction_data['match_id'] = prediction.match_id
        prediction_data['result'] = prediction.result
        output.append(prediction_data)
    return jsonify({'predictions': output})


@app.route('/predictions/<id>', methods=['PUT'])
def update_prediction(id):
    data = request.get_json()
    if not data or 'result' not in data:
        return jsonify({'message': 'Bad request'}), 400
    prediction = Prediction.query.get(id)
    if not prediction:
        return jsonify({'message': 'Prediction not found'})
    if data['result'] not in ['1', 'X', '2']:
        return jsonify({'message': 'Invalid result. Must be "1", "X", or "2"'})
    prediction.result = data['result']
    db.session.commit()
    return jsonify({'message': 'Prediction updated'})


@app.route('/predictions/<id>', methods=['DELETE'])
def delete_prediction(id):
    prediction = Prediction.query.get(id)
    if not prediction:
        return jsonify({'message': 'Prediction not found'})
    db.session.delete(prediction)
    db.session.commit()
    return jsonify({'message': 'Prediction deleted'})


@app.route('/matches', methods=['GET'])
def get_matches():
    response = requests.get('https://api.football-data.org/v2/competitions/PL/matches',
                            headers={'X-Auth-Token': API_KEY})
    matches = response.json()['matches']
    for match in matches:
        match_in_db = Match.query.filter_by(id=match['id']).first()
        if not match_in_db:
            new_match = Match(id=match['id'], team1=match['homeTeam']['name'], team2=match['awayTeam']['name'])
            db.session.add(new_match)
            db.session.commit()
    return jsonify({'matches': matches})


@app.route('/teams', methods=['GET'])
def get_teams():
    response = requests.get('https://api.football-data.org/v2/competitions/PL/teams',
                            headers={'X-Auth-Token': API_KEY})
    teams = response.json()['teams']
    return jsonify({'teams': teams})


@app.route('/teams/<id>/players', methods=['GET'])
def get_team_players(id):
    response = requests.get(f'https://api.football-data.org/v2/teams/{id}',
                            headers={'X-Auth-Token': API_KEY})
    team = response.json()
    return jsonify({'team': team['name'], 'players': team['squad']})


@app.route('/matches/<id>/details', methods=['GET'])
def get_match_details(id):
    response = requests.get(f'https://api.football-data.org/v2/matches/{id}',
                            headers={'X-Auth-Token': API_KEY})
    match = response.json()['match']
    return jsonify({'match': match})


@app.route('/matches/upcoming', methods=['GET'])
def get_upcoming_matches():
    response = requests.get('https://api.football-data.org/v2/competitions/PL/matches?status=SCHEDULED',
                            headers={'X-Auth-Token': API_KEY})
    matches = response.json()['matches']
    return jsonify({'matches': matches})


@app.route('/matches/completed', methods=['GET'])
def get_completed_matches():
    response = requests.get('https://api.football-data.org/v2/competitions/PL/matches?status=FINISHED',
                            headers={'X-Auth-Token': API_KEY})
    matches = response.json()['matches']
    return jsonify({'matches': matches})


if __name__ == '__main__':
    app.run(debug=True)
