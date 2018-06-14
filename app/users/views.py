from functools import wraps
from flask import request, jsonify, Blueprint
# import jwt
from app.models import User, BlacklistToken
# import uuid
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

            data = User.decode_auth_token(token)
            if isinstance(data, int):
                current_user = User.query.filter_by(id=data).first()
            else:
                return jsonify({'message': 'Invalid Token!'}), 401

            return f(current_user, *args, **kwargs)

    return decorated


@users_blueprint.route('/', methods=['POST', 'GET', 'PUT', 'DELETE'])
def index():
    response = jsonify({'greetings': 'Greetings and welcome to weConnect API'})
    return response, 200


@users_blueprint.route('/api/v2/auth/register', methods=['POST', 'GET', 'PUT', 'DELETE'])
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
        return jsonify({'message': 'User already exists.'}), 401

    created_user = User(email=data['email'], username=data['username'], password=hashed_password)

    user_data = {
        'email': created_user.email,
        'username': created_user.username,
        'user_id': created_user.id
    }

    db.session.add(created_user)
    db.session.commit()

    return jsonify({'message': 'New User Created', 'user_data': user_data}), 201


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
def logout(current_user):
    """Logs out the user and adds token to blacklist"""
    if not current_user:
        return jsonify({'message': 'You cannot perform this function'})

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


@users_blueprint.route('/api/v2/auth/reset-password', methods=['PUT'])
@token_required
def reset_password(current_user):
    if not current_user:
        return jsonify({'message': 'You cannot perform that function'})

    data = request.get_json()
    email = data.get('email')
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    confirm_password = data.get('confirm_password')

    if email is None:
        return jsonify({'msg': 'Please enter your email'}), 401
    if old_password is None:
        return jsonify({'msg': 'Please enter your old password.'}), 401
    if new_password is None:
        return jsonify({'msg': 'Please enter your new password.'}), 401
    if confirm_password is None:
        return jsonify({'msg': 'Please confirm your password.'}), 401

    if re.match("^[a-zA-Z0-9_]*$", new_password):
        return jsonify({"msg": "Your password should have at least 1 capital letter, special character and number."}), \
               401

    user = User.query.filter_by(email=email).first()

    if user.password:
        if confirm_password == new_password:
            user.password = generate_password_hash(new_password, method='sha256')
            db.session.add(user)
            db.session.commit()

            return jsonify({'message': 'Password successfully reset.'}), 200
        return jsonify({'message': 'Passwords do not match.', 'password': user.password}), 401
    return jsonify({'message': 'User not found.'}), 400
