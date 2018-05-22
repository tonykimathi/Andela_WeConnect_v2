from functools import wraps
from flask import request, jsonify, Blueprint
# import jwt
from app.models import User, BlacklistToken
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
# import datetime
import re

users_blueprint = Blueprint('users', __name__)
SECRET_KEY = 'BetterKeepThisSecret'


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.headers.get('Authorization'):
            header = request.headers.get('Authorization')
            token = header.split(" ")[1]

            if not token:
                return jsonify({'message': 'Token is missing!'}), 401

            return f(*args, **kwargs)

        return jsonify({'message': 'Token is invalid!'}), 401

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
        return jsonify({'message': 'Person already exists'}), 202

    created_user = User(email=data['email'], username=data['username'], password=hashed_password)

    db.session.add(created_user)
    db.session.commit()

    auth_token = created_user.encode_auth_token(created_user.id)

    return jsonify({'message': 'New User Created',
                    'auth_token': auth_token.decode()}), 201


@users_blueprint.route('/api/v2/auth/login', methods=['POST'])
def login():

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if email is None:
        return jsonify({"message": "Please input an email address"}), 401

    if password is None:
        return jsonify({"message": "Please input your password"}), 401

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'message': 'No user found'}), 404

    if check_password_hash(user.password, password):
        auth_token = user.encode_auth_token(user.id)

        return jsonify({'auth_token': auth_token.decode(), 'message': 'User login successful'}), 200

    return jsonify({'message': 'Wrong password entered'}), 401


@users_blueprint.route('/api/v2/auth/logout', methods=['POST'])
@token_required
def logout():
    """Logs out the user and adds token to blacklist"""

    auth_header = request.headers.get('Authorization')

    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''

    if auth_token:
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            # mark the token as blacklisted
            blacklist_token = BlacklistToken(token=auth_token)
            try:
                # insert the token
                db.session.add(blacklist_token)
                db.session.commit()

                return jsonify({'message': 'Successfully logged out.'}), 200
            except Exception as e:
                return jsonify({'message': e}), 400
        else:
            return jsonify({'message': resp}), 401
    else:
        return jsonify({'message': 'Provide a valid auth token.'}), 403
