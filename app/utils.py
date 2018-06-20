import re
from flask import jsonify, request
from app.models import Business
from sqlalchemy import func


def check_missing_registration_inputs(email, username, password):
    if email is None:
        return jsonify({"message": "Please input an email address"}), 401
    if username is None:
        return jsonify({"message": "Please input a username."}), 401
    if password is None:
        return jsonify({"message": "Please input a password."}), 401


def check_missing_login_inputs(email, password):
    if email is None:
        return jsonify({"message": "Please input an email address"}), 401
    if password is None:
        return jsonify({"message": "Please input a password."}), 401


def check_missing_change_password_inputs(email, old_password, new_password, confirm_password):
    if email is None:
        return jsonify({"msg": "Please enter your email"}), 401
    if old_password is None:
        return jsonify({'msg': 'Please enter your old password.'}), 401
    if new_password is None:
        return jsonify({'msg': 'Please enter your new password.'}), 401
    if confirm_password is None:
        return jsonify({'msg': 'Please confirm your password.'}), 401


def check_password(password):
    if re.match("^[a-zA-Z0-9_]*$", password):
        return jsonify({"msg": "Your password should have at least 1 capital letter, "
                               "special character and number."}), 401


def check_email(email):
    if not re.match(r"(^[a-zA-Z0-9_.]+@[a-zA-Z0-9-]+\.[a-z]+$)", email):
        return jsonify({"message": "Please provide a valid email address"}), 401


def check_missing_business_registration_inputs(business_name, description, location, category):
    if business_name is None:
        return jsonify({"message": "Please input a business name."}), 401
    if description is None:
        return jsonify({"message": "Please input a description."}), 401
    if location is None:
        return jsonify({"message": "Please input a location."}), 401
    if category is None:
        return jsonify({"message": "Please input a category."}), 401


def check_missing_review_registration_inputs(review_name, body):
    if review_name is None:
        return jsonify({"message": "Please input a review name."}), 401
    if body is None:
        return jsonify({"message": "Please input a review body."}), 401


def filter_business():
    category = request.args.get('category')
    location = request.args.get('location')
    businesses = Business.query
    if category is not None and category.strip() != '':
        businesses = businesses.filter(func.lower(Business.category).like('%' + func.lower(category) + '%'))

    if location is not None and location.strip() != '':
        businesses = businesses.filter(func.lower(Business.location).like('%' + func.lower(location) + '%'))
