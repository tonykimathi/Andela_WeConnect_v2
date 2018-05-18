from functools import wraps
from flask import request, jsonify
import jwt
from app.models import User
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(user_id=data['user_id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/api/v1/auth/register', methods=['POST'])
def signup():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    created_user = User(user_id=str(uuid.uuid4()), email=data['email'], username=['username'], password=hashed_password)

    db.session.add(created_user)
    db.session.commit()

    return jsonify({'message': 'New User Created'})


@app.route('/')
def index():
    response = jsonify({'greetings': 'Greetings and welcome to weConnect API'})
    return response, 200
