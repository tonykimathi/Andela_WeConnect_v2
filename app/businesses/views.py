from flask import Blueprint, request, jsonify
from sqlalchemy import func
from app.users.views import token_required
from app import db
from app.models import Business

businesses_blueprint = Blueprint('businesses', __name__)


@businesses_blueprint.route('/api/v2/auth/businesses', methods=['POST'])
@token_required
def create_business(current_user):
    if not current_user:
        return jsonify({'message': 'You cannot perform this function'})
    data = request.get_json()
    business_name = data.get('business_name')
    description = data.get('description')
    location = data.get('location')
    category = data.get('category')
    user_id = current_user.id

    if business_name is None:
        return jsonify({"message": "Please input a business name."}), 400
    if description is None:
        return jsonify({"message": "Please input a description."}), 400
    if location is None:
        return jsonify({"message": "Please input a location."}), 400
    if category is None:
        return jsonify({"message": "Please input a category."}), 400

    business = Business.query.filter_by(business_name=business_name).first()

    if business:
        return jsonify({'message': 'The business name you entered has been taken.'}), 202
    try:
        created_business = Business(business_name=business_name, description=description,
                                    location=location, category=category, user_id=user_id)
        db.session.add(created_business)
        db.session.commit()
        biz_data = {
            'business_id': created_business.business_id,
            'business_name': created_business.business_name,
            'description': created_business.description,
            'category': created_business.category,
            'location': created_business.location,
            'user_id': created_business.user_id
        }

    except KeyError:
        return jsonify({"message": "There is a missing field. Please check your inputs."}), 404
    return jsonify({'message': 'Business created successfully', 'business_data': biz_data}), 201


@businesses_blueprint.route('/api/v2/auth/businesses/<business_id>', methods=['PUT'])
@token_required
def update_business(current_user, business_id):
    if not current_user:
        return jsonify({'message': 'You cannot perform this function'})

    current_business = Business.query.filter_by(business_id=business_id).first()
    if current_business:
        data = request.get_json()
        business_name = data.get('business_name')
        description = data.get('description')
        location = data.get('location')
        category = data.get('category')
        user_id = current_user.id

        current_business.business_name = business_name
        current_business.description = description
        current_business.location = location
        current_business.category = category
        current_business.user_id = user_id

        db.session.add(current_business)
        db.session.commit()

        biz_data = {
            'business_id': current_business.business_id,
            'business_name': current_business.business_name,
            'description': current_business.description,
            'category': current_business.category,
            'location': current_business.location,
            'user_id': current_business.user_id
        }

        return jsonify({'message': 'Business updated successfully', 'business_data': biz_data}), 200
    return jsonify({'message': 'Business entered does not exist'}), 403


@businesses_blueprint.route('/api/v2/auth/businesses', methods=['GET'])
@token_required
def view_all_business(current_user):
    if not current_user:
        return jsonify({'message': 'You cannot perform this function'})

    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 2, type=int)
    search = request.args.get('q')
    category = request.args.get('category')
    location = request.args.get('location')
    all_businesses = Business.query

    if search is not None and search.strip() != '':
        all_businesses = all_businesses.filter(func.lower(
            Business.business_name).like('%' + func.lower(search) + '%'))

    if category is not None and category.strip() != '':
        all_businesses = all_businesses.filter(func.lower(
            Business.category).like('%' + func.lower(category) + '%'))

    if location is not None and location.strip() != '':
        all_businesses = all_businesses.filter(func.lower(
            Business.location).like('%' + func.lower(location) + '%'))

    businesses = all_businesses.paginate(page, limit, False)
    result = []

    for biz in businesses.items:
        biz_data = {
            'business_id': biz.business_id,
            'business_name': biz.business_name,
            'description': biz.description,
            'category': biz.category,
            'location': biz.location,
            'user_id': biz.user_id
        }
        result.append(biz_data)
    return jsonify({'all_businesses': result}), 200


@businesses_blueprint.route('/api/v2/auth/businesses/<business_id>', methods=['GET'])
@token_required
def view_single_business(current_user, business_id):
    if not current_user:
        return jsonify({'message': 'You cannot perform this function'})

    business = Business.query.filter_by(business_id=business_id).first()
    biz_data = {
        'business_id': business.business_id,
        'business_name': business.business_name,
        'description': business.description,
        'category': business.category,
        'location': business.location,
        'user_id': current_user.id
    }
    return jsonify({'single_business': biz_data}), 200


@businesses_blueprint.route('/api/v2/auth/businesses/<business_id>', methods=['DELETE'])
@token_required
def delete_single_business(current_user, business_id):
    if not current_user:
        return jsonify({'message': 'You cannot perform this function'})
    business = Business.query.filter_by(business_id=business_id).first()
    db.session.delete(business)
    db.session.commit()
    return jsonify({'message': 'Business successfully deleted'}), 200
