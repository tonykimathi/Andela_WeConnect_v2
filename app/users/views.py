from functools import wraps
from flask import request, jsonify, Blueprint, make_response
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

    valid_email = re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email.strip())
    hashed_password = generate_password_hash(data['password'], method='sha256')

    if valid_email is False:
        return jsonify({'message': 'Please enter valid Email!'}), 400

    if email is None:
        return jsonify({'message': 'Please input an email address'})

    if password is None:
        return jsonify({'message': 'Please input a password'})

    if username is None:
        return jsonify({'message': 'Please input a username'})

    person = User.query.filter_by(email=email).first()

    if person:
        return jsonify({'message': 'Person already exists'})

    created_user = User(user_id=str(uuid.uuid4()), email=data['email'], username=['username'], password=hashed_password)

    db.session.add(created_user)
    db.session.commit()

    return jsonify({'message': 'New User Created'}), 201



