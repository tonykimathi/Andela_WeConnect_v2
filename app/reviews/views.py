from flask import Blueprint, request, jsonify
from app.users.views import token_required
from app import db
from app.models import Review, Business

reviews_blueprint = Blueprint('reviews', __name__)


@reviews_blueprint.route('/api/v2/auth/businesses/<business_id>/reviews', methods=['POST', 'GET', 'PUT', 'DELETE'])
@token_required
def create_review(current_user, business_id):
    if not current_user:
        return jsonify({'message': 'You cannot perform this function'})
    if request.method == 'POST':

        business = Business.query.filter_by(business_id=business_id).first()

        data = request.get_json()
        # business_id = data.get('business_id')
        review_name = data.get('review_name')
        body = data.get('body')
        user_id = current_user.id

        if not business:
            return jsonify({'message': 'That business does not exist'}), 404
        if business.user_id == user_id:
            return jsonify({'message': 'You cannot review a business you own.'}), 403
        try:
            created_review = Review(review_name=review_name,
                                    body=body, user_id=user_id)
            db.session.add(created_review)
            db.session.commit()
            review_data = {
                'review_name': created_review.review_name,
                'body': created_review.body,
                'user_id': created_review.user_id
            }
        except KeyError:
            return jsonify({"message": "There is a missing field. Please check your inputs."}), 404
        return jsonify({'message': 'Review created successfully', 'business_data': review_data}), 201
    return jsonify({'message': 'Only GET and POST methods allowed.'})


@reviews_blueprint.route('/api/v2/auth/businesses/<business_id>/reviews', methods=['GET', 'POST', 'PUT', 'DELETE'])
@token_required
def get_all_reviews(current_user, business_id):
    if not current_user:
        return jsonify({'message': 'You cannot perform this function'})

    if request.method == 'GET':
        business = Business.query.filter_by(business_id=business_id).first()
        review_data = {
            'business_id': business.business_id,
            'review_name': business.review_name,
            'body': business.body,
            'user_id': business.user_id
        }
        return jsonify({'single_business': review_data}), 200
    else:
        return jsonify({'message': 'Only GET and POST methods allowed.'})
