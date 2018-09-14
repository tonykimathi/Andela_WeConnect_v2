from functools import wraps
from flask import request, jsonify, Blueprint
from app.utils import check_email, check_missing_registration_inputs, \
    check_missing_change_password_inputs, check_missing_login_inputs, \
    check_password


# import jwt
from app.models import User, BlacklistToken
# import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
# import datetime

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
        return jsonify({'message': 'No token found!'}), 401

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
    confirm_password = data.get('confirm_password')

    if password != confirm_password:
        return jsonify({'message': 'Passwords do not match'}), 401

    hashed_password = generate_password_hash(data['password'], method='sha256')
    confirm_hashed_password = generate_password_hash(data['confirm_password'], method='sha256')

    if check_missing_registration_inputs(email, username, password, confirm_password):
        return check_missing_registration_inputs(email, username, password, confirm_password)

    if check_email(email):
        return check_email(email)

    person = User.query.filter_by(email=email).first()

    if person:
        return jsonify({'message': 'User already exists.'}), 401

    created_user = User(email=data['email'], username=data['username'], password=hashed_password,
                        confirm_password=confirm_hashed_password)

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

    if check_missing_login_inputs(email, password):
        return check_missing_login_inputs(email, password)

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'message': 'No user found'}), 404

    if check_password_hash(user.password, password):
        auth_token = user.encode_auth_token(user.id)

        return jsonify({'auth_token': auth_token.decode(), 'message': 'User login successful'}), 200

    return jsonify({'message': 'Wrong email/password entered'}), 401


@users_blueprint.route('/api/v2/auth/logout', methods=['POST'])
@token_required
def logout(current_user):
    """Logs out the user and adds token to blacklist"""
    if current_user:

        auth_header = request.headers.get('Authorization')

        if auth_header:
            auth_token = auth_header.split(" ")[1]

            if auth_token:
                # mark the token as blacklisted
                blacklist_token = BlacklistToken(token=auth_token)

                # insert the token
                db.session.add(blacklist_token)
                db.session.commit()

                return jsonify({'message': 'Successfully logged out.'}), 200


@users_blueprint.route('/api/v2/auth/reset-password', methods=['PUT'])
@token_required
def reset_password():

    data = request.get_json()
    email = data.get('email')
    new_password = data.get('new_password')
    confirm_password = data.get('confirm_password')

    if check_missing_change_password_inputs(email, new_password, confirm_password):
        return check_missing_change_password_inputs(email, new_password, confirm_password)

    if check_email(email):
        return check_email(email)

    if check_password(new_password):
        return check_password(new_password)

    user = User.query.filter_by(email=email).first()

    if user:
        if confirm_password == new_password:
            user.password = generate_password_hash(new_password, method='sha256')
            db.session.add(user)
            db.session.commit()

            return jsonify({'message': 'Password successfully reset.'}), 200
        return jsonify({'message': 'Passwords do not match.'}), 401
    return jsonify({'message': 'User not found.'}), 400
