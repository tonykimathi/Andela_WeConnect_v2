from flask import Blueprint, request, jsonify
from sqlalchemy import func
from app.users.views import token_required
from app import db
from app.models import Business
from app.utils import check_missing_business_registration_inputs, filter_business

businesses_blueprint = Blueprint('businesses', __name__)


@businesses_blueprint.route('/api/v2/auth/businesses', methods=['POST'])
@token_required
def create_business(current_user):
    if current_user:

        data = request.get_json()
        business_name = data.get('business_name')
        description = data.get('description')
        location = data.get('location')
        category = data.get('category')
        user_id = current_user.id

        if check_missing_business_registration_inputs(business_name, description, location, category):
            return check_missing_business_registration_inputs(business_name, description, location, category)

        business = Business.query.filter_by(business_name=business_name).first()

        if business:
            return jsonify({'message': 'The business name you entered has been taken.'}), 202

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

        return jsonify({'message': 'Business created successfully', 'business_data': biz_data}), 201


@businesses_blueprint.route('/api/v2/auth/businesses/<business_id>', methods=['PUT'])
@token_required
def update_business(current_user, business_id):
    if current_user:
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
                'business_id': current_business.business_id, 'business_name': current_business.business_name,
                'description': current_business.description, 'category': current_business.category,
                'location': current_business.location, 'user_id': current_business.user_id
            }

            return jsonify({'message': 'Business updated successfully', 'business_data': biz_data}), 200
        return jsonify({'message': 'Business entered does not exist'}), 403


@businesses_blueprint.route('/api/v2/auth/businesses', methods=['GET'])
def view_all_business():

    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 6, type=int)
    search = request.args.get('q')

    businesses = Business.query

    if search is not None and search.strip() != '':
        businesses = businesses.filter(func.lower(Business.business_name).like('%' + func.lower(search) + '%'))

    if filter_business():
        return filter_business()

    paginated_businesses = businesses.paginate(page, limit, False)
    result = []

    for biz in paginated_businesses.items:
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
def view_single_business(business_id):

    business = Business.query.filter_by(business_id=business_id).first()
    biz_data = {
        'business_id': business.business_id,
        'business_name': business.business_name,
        'description': business.description,
        'category': business.category,
        'location': business.location,
        'user_id': business.user_id
    }
    return jsonify({'single_business': biz_data}), 200


@businesses_blueprint.route('/api/v2/auth/businesses/<business_id>', methods=['DELETE'])
@token_required
def delete_single_business(current_user, business_id):

    if current_user:

        business = Business.query.filter_by(business_id=business_id).first()
        db.session.delete(business)
        db.session.commit()
        return jsonify({'message': 'Business successfully deleted'}), 204
