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

# @businesses_blueprint.route('/api/v2/auth/businesses', methods=['PUT'])
# @token_required
# def update_business():

