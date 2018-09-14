import unittest
import json
import time
from app.models import db, BlacklistToken
from tests.base_test import BaseTestCase


class UsersTestCase(BaseTestCase):

    def test_successful_registration(self):
        response = self.client.post("/api/v2/auth/register", data=json.dumps(self.create_user), content_type=self.type)
        self.assertEqual(response.status_code, 201)
        response_message = json.loads(response.data.decode())
        self.assertEqual(response_message['message'], 'New User Created')
        response2 = self.client.post("/api/v2/auth/register", data=json.dumps(self.create_user), content_type=self.type)
        self.assertEqual(response2.status_code, 401)
        response_message2 = json.loads(response2.data.decode())
        self.assertEqual(response_message2['message'], 'User already exists.')

    def test_wrong_email_registration(self):
        response = self.client.post("/api/v2/auth/register", data=json.dumps(self.create_user2), content_type=self.type)
        self.assertEqual(response.status_code, 401)
        response_message = json.loads(response.data.decode())['message']
        self.assertEqual(response_message, 'Please provide a valid email address')

    def test_null_details_registration(self):
        response = self.client.post("/api/v2/auth/register", data=json.dumps(self.null_reg_create_user),
                                    content_type=self.type)
        response2 = self.client.post("/api/v2/auth/register", data=json.dumps(self.null_reg_create_user2),
                                     content_type=self.type)
        response3 = self.client.post("/api/v2/auth/register", data=json.dumps(self.null_reg_create_user3),
                                     content_type=self.type)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response2.status_code, 401)
        self.assertEqual(response3.status_code, 401)
        response_message = json.loads(response.data.decode())['message']
        response_message2 = json.loads(response2.data.decode())['message']
        response_message3 = json.loads(response3.data.decode())['message']
        self.assertEqual(response_message, 'Please input an email address')
        self.assertEqual(response_message2, 'Please input a username.')
        self.assertEqual(response_message3, 'Please input a password.')

    def test_successful_login(self):
        self.client.post("/api/v2/auth/register", data=json.dumps(self.login_create_user), content_type=self.type)
        response = self.client.post("/api/v2/auth/login", data=json.dumps(self.login_create_user),
                                    content_type=self.type)
        self.assertEqual(response.status_code, 200)
        response_message = json.loads(response.data.decode())
        self.assertEqual(response_message['message'], 'User login successful')
        self.assertTrue(response_message['auth_token'])

    def test_failed_login(self):
        response = self.client.post("/api/v2/auth/login", data=json.dumps(self.failed_login_user),
                                    content_type=self.type)
        self.assertEqual(response.status_code, 404)
        response_message = json.loads(response.data.decode())['message']
        self.assertEqual(response_message, 'No user found')

    def test_wrong_credentials_login(self):
        self.client.post("/api/v2/auth/register", data=json.dumps(self.wrong_login_create_user), content_type=self.type)
        no_email_login = {"email": None, "password": "tom12345"}
        response = self.client.post("/api/v2/auth/login", data=json.dumps(no_email_login), content_type=self.type)
        self.assertEqual(response.status_code, 401)
        response_message = json.loads(response.data.decode())['message']
        self.assertEqual(response_message, 'Please input an email address')

    def test_no_password_login(self):
        self.client.post("/api/v2/auth/register", data=json.dumps(self.no_password_create_user), content_type=self.type)
        response = self.client.post("/api/v2/auth/login", data=json.dumps(self.no_password_login),
                                    content_type=self.type)
        self.assertEqual(response.status_code, 401)
        response_message = json.loads(response.data.decode())['message']
        self.assertEqual(response_message, 'Please input a password.')

    def test_wrong_password_login(self):
        self.client.post("/api/v2/auth/register", data=json.dumps(self.wrong_password_user), content_type=self.type)
        response = self.client.post("/api/v2/auth/login", data=json.dumps(self.wrong_password_login_user),
                                    content_type=self.type)
        self.assertEqual(response.status_code, 401)
        response_message = json.loads(response.data.decode())['message']
        self.assertEqual(response_message, 'Wrong password entered')

    def test_successful_logout(self):
        self.client.post("/api/v2/auth/register", data=json.dumps(self.logout_create_user), content_type=self.type)
        login_response = self.client.post("/api/v2/auth/login", data=json.dumps(self.logout_create_user),
                                          content_type=self.type)
        response = self.client.post("/api/v2/auth/logout", content_type=self.type, headers=dict(
            Authorization="Bearer " + json.loads(login_response.data.decode())['auth_token']))
        response_message = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_message['message'], 'Successfully logged out.')

    # def test_invalid_logout(self):
    #     self.client.post("/api/v2/auth/register", data=json.dumps(self.invalid_logout_crete_user),
    #                      content_type=self.type)
    #     login_response = self.client.post("/api/v2/auth/login", data=json.dumps(self.invalid_logout_crete_user),
    #                                       content_type=self.type)
    #     time.sleep(300)
    #     response = self.client.post("/api/v2/auth/logout", content_type=self.type, headers=dict(
    #         Authorization="Bearer " + json.loads(login_response.data.decode())['auth_token']))
    #     response2 = self.client.post("/api/v2/auth/logout", content_type=self.type, headers=dict(
    #         Authorization="Bearer "))
    #     response3 = self.client.post("/api/v2/auth/logout", content_type=self.type)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response2.status_code, 401)
    #     self.assertEqual(response3.status_code, 401)
    #     response_message = json.loads(response.data.decode("utf-8"))
    #     response_message2 = json.loads(response2.data.decode("utf-8"))
    #     response_message3 = json.loads(response3.data.decode("utf-8"))
    #     self.assertEqual(response_message['message'], 'Invalid Token!')
    #     self.assertEqual(response_message2['message'], 'Token is missing!')
    #     self.assertEqual(response_message3['message'], 'No token found!')

    def test_valid_blacklisted_token_logout(self):
        """ Test for logout after a valid token gets blacklisted  """
        with self.client:
            self.client.post("/api/v2/auth/register", data=json.dumps(self.invalid_logout),
                             content_type=self.type)
            login_response = self.client.post("/api/v2/auth/login",
                                              data=json.dumps(self.invalid_logout), content_type=self.type)
            # blacklist a valid token
            blacklist_token = BlacklistToken(token=json.loads(login_response.data.decode())['auth_token'])
            db.session.add(blacklist_token)
            db.session.commit()
            # blacklisted valid token logout
            response = self.client.post('/api/v2/auth/businesses', headers=dict(
                Authorization='Bearer ' + json.loads(login_response.data.decode())['auth_token']))
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Invalid Token!')
            self.assertEqual(response.status_code, 401)

    def test_reset_password(self):
        with self.client:
            self.client.post("/api/v2/auth/register", data=json.dumps(self.reset_pass_create_user),
                             content_type="application/json")
            login_response = self.client.post("/api/v2/auth/login", data=json.dumps(self.reset_pass_create_user),
                                              content_type=self.type)
            self.header = dict(
                Authorization='Bearer ' + json.loads(login_response.data.decode())['auth_token'])
            reset_response = self.client.put("/api/v2/auth/reset-password", data=json.dumps(self.succ_password_reset),
                                             content_type=self.type, headers=self.header)
            reset_response2 = self.client.put("/api/v2/auth/reset-password", data=json.dumps(self.succ_password_reset2),
                                              content_type=self.type, headers=self.header)
            data = json.loads(reset_response.data.decode())
            data2 = json.loads(reset_response2.data.decode())
            self.assertEqual(data['message'], 'Password successfully reset.')
            self.assertEqual(data2['msg'], 'Your password should have at least 1 capital letter, '
                                           'special character and number.')
            self.assertEqual(reset_response.status_code, 200)
            self.assertEqual(reset_response2.status_code, 401)

    def test_failed_reset_password(self):
        with self.client:
            self.client.post("/api/v2/auth/register", data=json.dumps(self.reset_pass_user), content_type=self.type)
            login_response = self.client.post("/api/v2/auth/login", data=json.dumps(self.reset_pass_user),
                                              content_type=self.type)
            self.header = dict(
                Authorization='Bearer ' + json.loads(login_response.data.decode())['auth_token'])
            self.response = self.client.put("/api/v2/auth/reset-password", data=json.dumps(self.password_reset),
                                            content_type=self.type, headers=self.header)
            self.response2 = self.client.put("/api/v2/auth/reset-password", data=json.dumps(self.password_reset2),
                                             content_type=self.type, headers=self.header)
            self.response3 = self.client.put("/api/v2/auth/reset-password", data=json.dumps(self.password_reset3),
                                             content_type=self.type, headers=self.header)
            self.response4 = self.client.put("/api/v2/auth/reset-password", data=json.dumps(self.password_reset4),
                                             content_type=self.type, headers=self.header)
            self.response5 = self.client.put("/api/v2/auth/reset-password", data=json.dumps(self.password_reset5),
                                             content_type=self.type, headers=self.header)
            self.response6 = self.client.put("/api/v2/auth/reset-password", data=json.dumps(self.password_reset6),
                                             content_type=self.type, headers=self.header)
            data = json.loads(self.response.data.decode())
            data2 = json.loads(self.response2.data.decode())
            data3 = json.loads(self.response3.data.decode())
            data4 = json.loads(self.response4.data.decode())
            data5 = json.loads(self.response5.data.decode())
            data6 = json.loads(self.response6.data.decode())
            self.assertEqual(data['msg'], 'Please enter your email')
            self.assertEqual(data2['msg'], 'Please enter your old password.')
            self.assertEqual(data3['msg'], 'Please enter your new password.')
            self.assertEqual(data4['msg'], 'Please confirm your password.')
            self.assertEqual(data5['message'], 'Passwords do not match.')
            self.assertEqual(data6['message'], 'User not found.')

            self.assertEqual(self.response.status_code, 401), self.assertEqual(self.response2.status_code, 401)
            self.assertEqual(self.response3.status_code, 401), self.assertEqual(self.response4.status_code, 401)
            self.assertEqual(self.response5.status_code, 401), self.assertEqual(self.response6.status_code, 400)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.drop_all()
            db.session.remove()


if __name__ == '__main__':
    unittest.main()
