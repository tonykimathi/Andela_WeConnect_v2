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

    def test_successful_business_review(self):
        create_user = {"email": "tomgeeF@email.com",
                       "username": "TomGiF",
                       "password": "tim12345"
                       }

        self.client.post("/api/v2/auth/register",
                         data=json.dumps(create_user),
                         content_type="application/json")

        login_response2 = self.client.post("/api/v2/auth/login",
                                          data=json.dumps(create_user),
                                          content_type="application/json")
        create_business = {"business_name": "St. Pius The Tenth",
                           "description": "This is a school founded in 2015",
                           "category": "School",
                           "location": "Meru"
                           }

        self.client.post("/api/v2/auth/businesses",
                         data=json.dumps(create_business),
                         content_type="application/json",
                         headers=dict(
                             Authorization='Bearer ' + json.loads(
                                 login_response2.data.decode()
                             )['auth_token']
                         ))
        own_review = {"review_name": "School Review",
                      "body": "St. Pius is a very high performing school."
                      }
        own_review_response = self.client.post("/api/v2/auth/businesses/1/reviews",
                                               data=json.dumps(own_review),
                                               content_type="application/json",
                                               headers=dict(
                                                   Authorization='Bearer ' +
                                                                 json.loads(login_response2.data.decode())
                                                                 ['auth_token']
                                               ))
        own_review_data = json.loads(own_review_response.data.decode())
        self.assertEqual(own_review_data['message'], "You cannot review a business you own.")
        self.assertEqual(own_review_response.status_code, 403)

        create_user = {"email": "tonyFee@email.com",
                       "username": "TonyFee",
                       "password": "tim12345"
                       }

        self.client.post("/api/v2/auth/register",
                         data=json.dumps(create_user),
                         content_type="application/json")

        login_response = self.client.post("/api/v2/auth/login",
                                          data=json.dumps(create_user),
                                          content_type="application/json")

        create_review = {"review_name": "School Review",
                         "body": "St. Pius is a very high performing school."
                         }
        error_review = {"review_name": None,
                        "body": "St. Pius X is a very high performing school."
                        }
        error_review2 = {"review_name": "School Review",
                         "body": None
                         }
        review_response = self.client.post("/api/v2/auth/businesses/1/reviews",
                                           data=json.dumps(create_review),
                                           content_type="application/json",
                                           headers=dict(
                                               Authorization='Bearer ' + json.loads(
                                                   login_response.data.decode()
                                               )['auth_token']
                                           ))
        no_business_review_response = self.client.post("/api/v2/auth/businesses/7/reviews",
                                           data=json.dumps(create_review),
                                           content_type="application/json",
                                           headers=dict(
                                               Authorization='Bearer ' + json.loads(
                                                   login_response.data.decode()
                                               )['auth_token']
                                           ))
        error_response = self.client.post("/api/v2/auth/businesses/1/reviews",
                                          data=json.dumps(error_review),
                                          content_type="application/json",
                                          headers=dict(
                                              Authorization='Bearer ' + json.loads(
                                                  login_response.data.decode()
                                              )['auth_token']
                                          ))
        error_response2 = self.client.post("/api/v2/auth/businesses/1/reviews",
                                           data=json.dumps(error_review2),
                                           content_type="application/json",
                                           headers=dict(
                                               Authorization='Bearer ' + json.loads(
                                                   login_response.data.decode()
                                               )['auth_token']
                                           ))
        get_response = self.client.get("/api/v2/auth/businesses/1/reviews",
                                       content_type="application/json",
                                       headers=dict(
                                           Authorization='Bearer ' + json.loads(
                                               login_response.data.decode()
                                           )['auth_token']
                                       ))

        data = json.loads(review_response.data.decode())
        data0 = json.loads(no_business_review_response.data.decode())
        data1 = json.loads(get_response.data.decode())
        data2 = json.loads(error_response.data.decode())
        data3 = json.loads(error_response2.data.decode())

        self.assertEqual(data['message'], "Review created successfully")
        self.assertEqual(review_response.status_code, 201)

        self.assertEqual(data0['message'], "That business does not exist")
        self.assertEqual(no_business_review_response.status_code, 404)

        self.assertEqual(data1['message'], "These are your reviews.")
        self.assertEqual(get_response.status_code, 200)

        self.assertEqual(data2['message'], "Please input a review name.")
        self.assertEqual(data3['message'], "Please input a review body.")
        self.assertEqual(error_response.status_code, 401)
        self.assertEqual(error_response2.status_code, 401)
