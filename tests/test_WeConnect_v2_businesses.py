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

    def test_successful_business_registration(self):
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
                           "location": "Meru"
                           }

        business_response = self.client.post("/api/v2/auth/businesses",
                                             data=json.dumps(create_business),
                                             content_type="application/json",
                                             headers=dict(
                                                 Authorization='Bearer ' + json.loads(
                                                     login_response.data.decode()
                                                 )['auth_token']
                                             ))
        data = json.loads(business_response.data.decode())
        self.assertEqual(data['message'], "Business created successfully")
        self.assertEqual(business_response.status_code, 201)

    def test_successful_business_update(self):
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
                           "location": "Meru"
                           }

        self.client.post("/api/v2/auth/businesses",
                         data=json.dumps(create_business),
                         content_type="application/json",
                         headers=dict(
                             Authorization='Bearer ' + json.loads(
                                 login_response.data.decode()
                             )['auth_token']
                         ))
        update_business = {"business_name": "St. Pius The Tenth Academy",
                           "description": "This is a school founded in 2017",
                           "category": "School",
                           "location": "Meru"
                           }
        update_response = self.client.put("/api/v2/auth/businesses/1",
                                          data=json.dumps(update_business),
                                          content_type="application/json",
                                          headers=dict(
                                              Authorization='Bearer ' + json.loads(
                                                  login_response.data.decode()
                                              )['auth_token']
                                          ))
        data = json.loads(update_response.data.decode())
        self.assertEqual(data['message'], "Business updated successfully")
        self.assertEqual(update_response.status_code, 200)

    def test_view_all_businesses(self):
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
                           "location": "Meru"
                           }
        create_business2 = {"business_name": "Mimosa Clinics",
                            "description": "This is a clinic founded in 2017",
                            "category": "Clinic",
                            "location": "Nairobi"
                            }
        self.client.post("/api/v2/auth/businesses",
                         data=json.dumps(create_business),
                         content_type="application/json",
                         headers=dict(
                             Authorization='Bearer ' + json.loads(
                                 login_response.data.decode()
                             )['auth_token']
                         ))
        self.client.post("/api/v2/auth/businesses",
                         data=json.dumps(create_business2),
                         content_type="application/json",
                         headers=dict(
                             Authorization='Bearer ' + json.loads(
                                 login_response.data.decode()
                             )['auth_token']
                         ))

        business_response = self.client.get("/api/v2/auth/businesses",
                                            content_type="application/json",
                                            headers=dict(
                                                Authorization='Bearer ' + json.loads(
                                                    login_response.data.decode()
                                                )['auth_token']
                                            ))
        self.assertEqual(business_response.status_code, 200)

    def test_view_single_business(self):
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
                           "location": "Meru"
                           }

        self.client.post("/api/v2/auth/businesses",
                         data=json.dumps(create_business),
                         content_type="application/json",
                         headers=dict(
                             Authorization='Bearer ' + json.loads(
                                 login_response.data.decode()
                             )['auth_token']
                         ))

        business_response = self.client.get("/api/v2/auth/businesses/1",
                                            content_type="application/json",
                                            headers=dict(
                                                Authorization='Bearer ' + json.loads(
                                                    login_response.data.decode()
                                                )['auth_token']
                                            ))
        self.assertEqual(business_response.status_code, 200)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.drop_all()
            db.session.remove()


if __name__ == '__main__':
    unittest.main()
