from functools import wraps
from flask import request, jsonify, Blueprint
import jwt
from app.models import User
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
import datetime
import re

users_blueprint = Blueprint('users', __name__)
SECRET_KEY = 'BetterKeepThisSecret'


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, SECRET_KEY)
            current_user = User.query.filter_by(user_id=data['user_id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@users_blueprint.route('/')
def index():
    response = jsonify({'greetings': 'Greetings and welcome to weConnect API'})
    return response, 200


@users_blueprint.route('/api/v2/auth/register', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    hashed_password = generate_password_hash(data['password'], method='sha256')

    if email is None:
        return jsonify({"message": "Please input an email address"}), 400
    if username is None:
        return jsonify({"message": "Please input a username."}), 400
    if password is None:
        return jsonify({"message": "Please input a password."}), 400

    if not re.match(r"(^[a-zA-Z0-9_.]+@[a-zA-Z0-9-]+\.[a-z]+$)", email):
        return jsonify({"message": "Please provide a valid email address"}), 401

    person = User.query.filter_by(email=email).first()

    if person:
        return jsonify({'message': 'Person already exists'})

    created_user = User(user_id=str(uuid.uuid4()), email=data['email'], username=['username'], password=hashed_password)

    db.session.add(created_user)
    db.session.commit()

    return jsonify({'message': 'New User Created'}), 201


@users_blueprint.route('/api/v2/auth/login', methods=['POST'])
def login():

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if email is None:
        return jsonify({"message": "Please input an email address"}), 401

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'message': 'No user found'}), 401

    if check_password_hash(user.password, password):
        token = jwt.encode({'user_id': user.user_id,
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                           SECRET_KEY)

        return jsonify({'token': token.decode('UTF-8'), 'message': 'User login successful'}), 200

    return jsonify({'message': 'Wrong password entered'}), 401

#@users_blueprint.route('/api/v2/auth/login', methods=['POST'])
#def logout():
