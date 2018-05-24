import unittest
import json
from app import create_app
from app.models import db


class BusinessTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()

        with self.app.app_context():

            db.drop_all()
            db.create_all()

    def test_failed_business_review(self):
        create_user = {"email": "tomgeeF@email.com",
                       "username": "TomGiF",
                       "password": "tim12345"
                       }

        self.client.post("/api/v2/auth/register",
                         data=json.dumps(create_user),
                         content_type="application/json")

        login_response = self.client.post("/api/v2/auth/login",
                                          data=json.dumps(create_user),
                                          content_type="application/json")

        create_business = {"business_name": "St. Pius The Tenth",
                           "description": "This is a school founded in 2015",
                           "category": "School",
                           "location": "Meru",
                           "user_id": 1
                           }

        self.client.post("/api/v2/auth/businesses",
                         data=json.dumps(create_business),
                         content_type="application/json",
                         headers=dict(
                             Authorization='Bearer ' + json.loads(
                                 login_response.data.decode()
                             )['auth_token']
                         ))
        create_review = {"review_name": "School Review",
                         "body": "St. Pius is a very high performing school.",
                         "user_id": 1
                         }
        review_response = self.client.post("/api/v2/auth/businesses/1/reviews",
                                           data=json.dumps(create_review),
                                           content_type="application/json",
                                           headers=dict(
                                               Authorization='Bearer ' + json.loads(
                                                   login_response.data.decode()
                                               )['auth_token']
                                           ))

        data = json.loads(review_response.data.decode())
        self.assertEqual(data['message'], "You cannot review a business you own.")
        self.assertEqual(review_response.status_code, 403)
