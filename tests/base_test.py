"""
Base Test case with setup and methods that other
test classes inherit
"""
import unittest
import json
import datetime
from app import create_app, db
from app.models import User


class BaseTestCase(unittest.TestCase):
    """Base Test Case"""
    def setUp(self):
        """Set up test variables"""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        with self.app.app_context():
            db.drop_all()
            db.create_all()

            self.type = "application/json"
            self.create_user = {"email": "timgee@email.com", "username": "TimG", "password": "tim12345"}
            self.create_user2 = {"email": "timgee-emai-com", "username": "TimGi", "password": "tim12345"}
            self.null_reg_create_user = {"email": None, "username": "TimGI", "password": "tim12345"}
            self.null_reg_create_user2 = {"email": 'timgi@email.com', "username": None, "password": "tim12345"}
            self.null_reg_create_user3 = {"email": 'timgi@email.com', "username": "TimGI", "password": None}
            self.login_create_user = {"email": "timgee@email.com", "username": "TimGi", "password": "tim12345"}
            self.failed_login_user = {"email": "tomgee@email.com", "password": "tom12345"}
            self.wrong_login_create_user = {"email": "timgee@email.com", "username": "TimGi", "password": "tim12345"}

            self.reset_pass_create_user = {"email": "timgee@email.com", "username": "TimGi", "password": "Tim12345."}

            self.succ_password_reset = {"email": "timgee@email.com", "old_password": "Tim12345.",
                                   "new_password": "Tim123456-.", "confirm_password": "Tim123456-."}
            self.succ_password_reset2 = {"email": "timgee@email.com", "old_password": "Tim12345.",
                                    "new_password": "Tim123456", "confirm_password": "Tim123456"}

            self.password_reset = {"email": None, "old_password": "Tim12345.",
                                   "new_password": "Tim123456-.", "confirm_password": "Tim123456-."}
            self.password_reset2 = {"email": "timgee@email.com", "old_password": None,
                                    "new_password": "Tim123456-.", "confirm_password": "Tim123456-."}
            self.password_reset3 = {"email": "timgee@email.com", "old_password": "Tim12345.", "new_password": None,
                                    "confirm_password": "Tim123456-."}
            self.password_reset4 = {"email": "timgee@email.com", "old_password": "Tim12345.", "new_password": "Tim123456-.",
                                    "confirm_password": None}
            self.password_reset5 = {"email": "timgee@email.com", "old_password": "Tim12345.", "new_password": "Tim123456-.",
                                    "confirm_password": "Tim123456-.."}
            self.password_reset6 = {"email": "timgee1@email.com", "old_password": "Tim12345.",
                                    "new_password": "Tim123456-.", "confirm_password": "Tim123456-.."}
            self.create_user3 = {"email": "timgee@email.com", "username": "TimGi", "password": "Tim12345."}
            self.no_password_create_user = {"email": "timgee@email.com", "username": "TimGi", "password": "tim12345"}
            self.no_password_login = {"email": 'timgee@email.com', "password": None}
            self.wrong_password_user = {"email": "timgee@email.com", "username": "TimGi", "password": "tim12345"}
            self.wrong_password_login_user = {"email": "timgee@email.com", "password": "tom12345"}
            self.logout_create_user = {"email": "timgee@email.com", "username": "TimGi", "password": "tim12345"}
            self.invalid_logout_crete_user = {"email": "timgee@email.com", "username": "TimGi", "password": "tim12345"}
            self.invalid_logout = {"email": "timgee@email.com", "username": "TimGi", "password": "tim12345"}
            self.reset_pass_user = {"email": "timgee@email.com", "username": "TimGi", "password": "Tim12345."}


    def test_encode_auth_token(self):
        user = User(
            email='test@test.com',
            username='mic_testing',
            password='test',
        )
        with self.app.app_context():

            db.session.add(user)
            db.session.commit()
            auth_token = user.encode_auth_token(user.id)
            self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = User(
            email='test@test.com',
            username='mic_testing',
            password='test',
        )
        with self.app.app_context():

            db.session.add(user)
            db.session.commit()
            auth_token = user.encode_auth_token(user.id)
            self.assertTrue(isinstance(auth_token, bytes))
            self.assertTrue(User.decode_auth_token(auth_token) == 1)

    def test_home_page(self):
        response = self.client.get("/")
        response_message = json.loads(response.data.decode())['greetings']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_message, 'Greetings and welcome to weConnect API')
