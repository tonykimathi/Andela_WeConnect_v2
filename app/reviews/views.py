from flask import Blueprint, request, jsonify
from app.users.views import token_required
from app import db
from app.models import Review, Business
from app.utils import check_missing_review_registration_inputs

reviews_blueprint = Blueprint('reviews', __name__)


@reviews_blueprint.route('/api/v2/auth/businesses/<int:business_id>/reviews', methods=['POST'])
@token_required
def create_review(current_user, business_id):
    if current_user:

        if request.method == 'POST':

            business = Business.query.filter_by(business_id=business_id).first()

            data = request.get_json()
            print(data)
            body = data.get('body')
            user_id = current_user.id
            business_id = business.business_id

            if check_missing_review_registration_inputs(body):
                return check_missing_review_registration_inputs(body)

            if not business:
                return jsonify({'message': 'That business does not exist'}), 404
            if business.user_id == user_id:
                return jsonify({'message': 'You cannot review a business you own.'}), 403
            else:
                created_review = Review(body=body, user_id=user_id, business_id=business_id)
                db.session.add(created_review)
                db.session.commit()
                review_data = {
                    'body': created_review.body,
                    'user_id': created_review.user_id,
                    'review_id': created_review.review_id
                }
                return jsonify({'message': 'Review created successfully', 'review_data': review_data}), 201


@reviews_blueprint.route('/api/v2/auth/businesses/<int:business_id>/reviews', methods=['GET'])
def get_all_reviews(business_id):

    if request.method == 'GET':
        store = []
        reviews = Review.query.filter_by(business_id=business_id)
        for review in reviews:
            review_data = {
                'review_id': review.review_id,
                'body': review.body,
                'user_id': review.user_id
            }
            store.append(review_data)
        return jsonify({'data': store}), 200
