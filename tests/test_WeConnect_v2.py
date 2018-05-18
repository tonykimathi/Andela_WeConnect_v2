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

        create_user = {"email": "tonygee@email.com",
                       "username": "TonyG",
                       "password": "12345"
                       }

        self.client.post("/api/v2/auth/register",
                         data=json.dumps(create_user),
                         content_type="application/json")

        response = self.client.post("/api/v2/auth/login",
                                    data=json.dumps(create_user),
                                    content_type="application/json")

        print(json.loads(response.data.decode()))

        self.token = json.loads(response.data.decode())['token']

        self.headers = {'Content-Type': 'application/json',
                        'token': self.token}

    def test_successful_registration(self):
        create_user = {"email": "timgee@email.com",
                       "username": "TimG",
                       "password": "tim12345"
                       }

        response = self.client.post("/api/v2/auth/register",
                                    data=json.dumps(create_user),
                                    content_type="application/json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response['message'], 'New User Created')


