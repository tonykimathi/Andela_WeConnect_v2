import unittest
import json
from app import create_app
from app.models import db


class UsersTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()

        with self.app.app_context():

            db.create_all()

        # create_user = {"email": "tonygee@email.com",
                       # "username": "TonyG",
                       # "password": "12345"
                       # }

        # self.client.post("/api/v2/auth/register",
                         # data=json.dumps(create_user),
                         # content_type="application/json")

        # response = self.client.post("/api/v2/auth/login",
                                    # data=json.dumps(create_user),
                                    # content_type="application/json")

        # print(json.loads(response.data.decode()))

        # self.token = json.loads(response.data.decode())['token']

        # self.headers = {'Content-Type': 'application/json',
                        # 'token': self.token}

    def test_successful_registration(self):
        create_user = {"email": "timgee@email.com",
                       "username": "TimG",
                       "password": "tim12345"
                       }

        response = self.client.post("/api/v2/auth/register",
                                    data=json.dumps(create_user),
                                    content_type="application/json")

        self.assertEqual(response.status_code, 201)
        response_message = json.loads(response.data)['message']
        self.assertEqual(response_message, 'New User Created')

    def test_wrong_email_registration(self):
        create_user = {"email": "timgee-emai-com",
                       "username": "TimGi",
                       "password": "tim12345"
                       }

        response = self.client.post("/api/v2/auth/register",
                                    data=json.dumps(create_user),
                                    content_type="application/json")

        self.assertEqual(response.status_code, 401)
        response_message = json.loads(response.data)['message']
        self.assertEqual(response_message, 'Please provide a valid email address')

    def test_null_details_registration(self):
        create_user = {"email": None,
                       "username": "TimGI",
                       "password": "tim12345"
                       }

        response = self.client.post("/api/v2/auth/register",
                                    data=json.dumps(create_user),
                                    content_type="application/json")

        self.assertEqual(response.status_code, 400)
        response_message = json.loads(response.data)['message']
        self.assertEqual(response_message, 'Please input an email address')

    def test_successful_login(self):
        create_user = {"email": "timgee@email.com",
                       "username": "TimGi",
                       "password": "tim12345"
                       }

        self.client.post("/api/v2/auth/register",
                         data=json.dumps(create_user),
                         content_type="application/json")
        response = self.client.post("/api/v2/auth/login",
                                    data=json.dumps(create_user),
                                    content_type="application/json")

        self.assertEqual(response.status_code, 200)
        response_message = json.loads(response.data)['message']
        self.assertEqual(response_message, 'User login successful')

    def test_failed_login(self):
        failed_login_user = {"email": "tomgee@email.com",
                             "password": "tom12345"
                             }
        response = self.client.post("/api/v2/auth/login",
                                    data=json.dumps(failed_login_user),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 401)
        response_message = json.loads(response.data)['message']
        self.assertEqual(response_message, 'No user found')

    def test_wrong_credentials_login(self):
        create_user = {"email": "timgee@email.com",
                       "username": "TimGi",
                       "password": "tim12345"
                       }

        self.client.post("/api/v2/auth/register",
                         data=json.dumps(create_user),
                         content_type="application/json")
        no_email_login = {"email": None,
                          "password": "tom12345"
                         }
        response = self.client.post("/api/v2/auth/login",
                                    data=json.dumps(no_email_login),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 401)
        response_message = json.loads(response.data)['message']
        self.assertEqual(response_message, 'Please input an email address')

    def test_no_password_login(self):
        create_user = {"email": "timgee@email.com",
                       "username": "TimGi",
                       "password": "tim12345"
                       }

        self.client.post("/api/v2/auth/register",
                         data=json.dumps(create_user),
                         content_type="application/json")
        no_password_login = {"email": 'timgee@email.com',
                             "password": None
                            }
        response = self.client.post("/api/v2/auth/login",
                                    data=json.dumps(no_password_login),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 401)
        response_message = json.loads(response.data)['message']
        self.assertEqual(response_message, 'Please input your password')

    def test_wrong_password_login(self):
        create_user = {"email": "timgee@email.com",
                       "username": "TimGi",
                       "password": "tim12345"
                       }

        self.client.post("/api/v2/auth/register",
                         data=json.dumps(create_user),
                         content_type="application/json")
        wrong_password_login_user = {"email": "timgee@email.com",
                                     "password": "tom12345"
                                     }
        response = self.client.post("/api/v2/auth/login",
                                    data=json.dumps(wrong_password_login_user),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 401)
        response_message = json.loads(response.data)['message']
        self.assertEqual(response_message, 'Wrong password entered')

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()

