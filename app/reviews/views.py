from flask import Blueprint, request, jsonify
from app.users.views import token_required
from app import db
from app.models import Review, Business

reviews_blueprint = Blueprint('reviews', __name__)


@reviews_blueprint.route('/api/v2/auth/businesses/<int:business_id>/reviews', methods=['POST'])
@token_required
def create_review(current_user, business_id):
    if current_user:

        if request.method == 'POST':

            business = Business.query.filter_by(business_id=business_id).first()

            data = request.get_json()
            review_name = data.get('review_name')
            body = data.get('body')
            user_id = current_user.id

            if review_name is None:
                return jsonify({"message": "Please input a review name."}), 400
            if body is None:
                return jsonify({"message": "Please input a review body."}), 400

            if not business:
                return jsonify({'message': 'That business does not exist'}), 404
            if business.user_id == user_id:
                return jsonify({'message': 'You cannot review a business you own.'}), 403

            created_review = Review(review_name=review_name,
                                    body=body, user_id=user_id)
            db.session.add(created_review)
            db.session.commit()
            review_data = {
                'review_name': created_review.review_name,
                'body': created_review.body,
                'user_id': created_review.user_id
            }
            return jsonify({'message': 'Review created successfully', 'business_data': review_data}), 201


@reviews_blueprint.route('/api/v2/auth/businesses/<int:business_id>/reviews', methods=['GET'])
@token_required
def get_all_reviews(current_user, business_id):
    if current_user:

        if request.method == 'GET':
            store = []
            reviews = Review.query
            for review in reviews:
                review_data = {
                    'business_id': review.review_id,
                    'review_name': review.review_name,
                    'body': review.body,
                    'user_id': review.user_id
                }
                store.append(review_data)
            return jsonify({'message': 'These are your reviews.', 'data': store}), 200
