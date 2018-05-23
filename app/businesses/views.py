from flask import Blueprint, request, jsonify
from app.users.views import token_required
from app import db
from app.models import Business

businesses_blueprint = Blueprint('businesses', __name__)


@businesses_blueprint.route('/api/v2/auth/businesses', methods=['POST'])
@token_required
def create_business():
    data = request.get_json()
    business_name = data.get('business_name')
    description = data.get('description')
    location = data.get('location')
    category = data.get('category')

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
                                    location=location, category=category)
        db.session.add(created_business)
        db.session.commit()
        biz_data = {
            'business_id': created_business.business_id,
            'business_name': created_business.business_name,
            'description': created_business.description,
            'category': created_business.category,
            'location': created_business.location
        }

    except KeyError:
        return jsonify({"message": "There is a missing field. Please check your inputs."}), 404
    return jsonify({'message': 'Business created successfully', 'business_data': biz_data}), 201


@businesses_blueprint.route('/api/v2/auth/businesses/<business_id>/', methods=['PUT'])
@token_required
def update_business(business_id):
    current_business = Business.query.filter_by(business_id=business_id).first()
    if current_business:
        data = request.get_json()
        business_name = data.get('business_name')
        description = data.get('description')
        location = data.get('location')
        category = data.get('category')

        try:
            new_business = Business.query.filter_by(business_name=business_name).first()

            if new_business:
                return jsonify({'message': 'Business name already exists, enter a new one.'}), 202

            current_business.business_name = business_name
            current_business.description = description
            current_business.location = location
            current_business.category = category

            db.session.add(current_business)
            db.session.commit()

            biz_data = {
                'business_id': current_business.business_id,
                'business_name': current_business.business_name,
                'description': current_business.description,
                'category': current_business.category,
                'location': current_business.location
            }

        except KeyError:
            return jsonify({"message": "There was an error updating your business, please try again."}), 404
        return jsonify({'message': 'Business updated successfully', 'business_data': biz_data}), 200


@businesses_blueprint.route('/api/v2/auth/businesses', methods=['GET'])
@token_required
def view_all_business():
    all_businesses = Business.query.all()
    result = []

    for biz in all_businesses:
        biz_data = {
            'business_id': biz.business_id,
            'business_name': biz.business_name,
            'description': biz.description,
            'category': biz.category,
            'location': biz.location
        }
        result.append(biz_data)
    return jsonify({'all_businesses': result}), 200


