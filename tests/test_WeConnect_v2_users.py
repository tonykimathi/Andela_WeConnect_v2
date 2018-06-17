import unittest
# import time
import json
from app import create_app
from app.models import db, User, BlacklistToken


class UsersTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()

        with self.app.app_context():

            db.drop_all()
            db.create_all()

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

    def test_successful_registration(self):
        create_user = {"email": "timgee@email.com",
                       "username": "TimG",
                       "password": "tim12345"
                       }

        response = self.client.post("/api/v2/auth/register",
                                    data=json.dumps(create_user),
                                    content_type="application/json")

        self.assertEqual(response.status_code, 201)
        response_message = json.loads(response.data.decode())
        self.assertEqual(response_message['message'], 'New User Created')

        response2 = self.client.post("/api/v2/auth/register",
                                     data=json.dumps(create_user),
                                     content_type="application/json")
        self.assertEqual(response2.status_code, 401)
        response_message2 = json.loads(response2.data.decode())
        self.assertEqual(response_message2['message'], 'User already exists.')

    def test_wrong_email_registration(self):
        create_user = {"email": "timgee-emai-com",
                       "username": "TimGi",
                       "password": "tim12345"
                       }

        response = self.client.post("/api/v2/auth/register",
                                    data=json.dumps(create_user),
                                    content_type="application/json")

        self.assertEqual(response.status_code, 401)
        response_message = json.loads(response.data.decode())['message']
        self.assertEqual(response_message, 'Please provide a valid email address')

    def test_null_details_registration(self):
        create_user = {"email": None,
                       "username": "TimGI",
                       "password": "tim12345"
                       }
        create_user2 = {"email": 'timgi@email.com',
                        "username": None,
                        "password": "tim12345"
                        }
        create_user3 = {"email": 'timgi@email.com',
                        "username": "TimGI",
                        "password": None
                        }

        response = self.client.post("/api/v2/auth/register",
                                    data=json.dumps(create_user),
                                    content_type="application/json")
        response2 = self.client.post("/api/v2/auth/register",
                                     data=json.dumps(create_user2),
                                     content_type="application/json")
        response3 = self.client.post("/api/v2/auth/register",
                                     data=json.dumps(create_user3),
                                     content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response2.status_code, 400)
        self.assertEqual(response3.status_code, 400)

        response_message = json.loads(response.data.decode())['message']
        response_message2 = json.loads(response2.data.decode())['message']
        response_message3 = json.loads(response3.data.decode())['message']

        self.assertEqual(response_message, 'Please input an email address')
        self.assertEqual(response_message2, 'Please input a username.')
        self.assertEqual(response_message3, 'Please input a password.')

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
        response_message = json.loads(response.data.decode())
        self.assertEqual(response_message['message'], 'User login successful')
        self.assertTrue(response_message['auth_token'])

    def test_failed_login(self):
        failed_login_user = {"email": "tomgee@email.com",
                             "password": "tom12345"
                             }
        response = self.client.post("/api/v2/auth/login",
                                    data=json.dumps(failed_login_user),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 404)
        response_message = json.loads(response.data.decode())['message']
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
        response_message = json.loads(response.data.decode())['message']
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
        response_message = json.loads(response.data.decode())['message']
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
        response_message = json.loads(response.data.decode())['message']
        self.assertEqual(response_message, 'Wrong password entered')

    def test_successful_logout(self):
        create_user = {"email": "timgee@email.com",
                       "username": "TimGi",
                       "password": "tim12345"
                       }

        self.client.post("/api/v2/auth/register",
                         data=json.dumps(create_user),
                         content_type="application/json")
        login_response = self.client.post("/api/v2/auth/login",
                                          data=json.dumps(create_user),
                                          content_type="application/json")
        response = self.client.post("/api/v2/auth/logout",
                                    content_type="application/json",
                                    headers=dict(
                                        Authorization="Bearer " + json.loads(login_response.data.decode())['auth_token']
                                    ))
        # print(json.loads(login_response.data.decode())['auth_token'])
        response_message = json.loads(response.data.decode())
        # print(response_message)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_message['message'], 'Successfully logged out.')

    def test_invalid_logout(self):
        create_user = {"email": "timgee@email.com",
                       "username": "TimGi",
                       "password": "tim12345"
                       }

        self.client.post("/api/v2/auth/register",
                         data=json.dumps(create_user),
                         content_type="application/json")
        login_response = self.client.post("/api/v2/auth/login",
                                          data=json.dumps(create_user),
                                          content_type="application/json")
        # time.sleep(660)
        response = self.client.post("/api/v2/auth/logout",
                                    content_type="application/json",
                                    headers=dict(
                                        Authorization="Bearer " +
                                                      json.loads(login_response.data.decode())['auth_token']
                                    ))
        response2 = self.client.post("/api/v2/auth/logout",
                                     content_type="application/json",
                                     headers=dict(
                                         Authorization="Bearer "
                                     ))

        # self.assertEqual(response.status_code, 401)
        self.assertEqual(response2.status_code, 401)

        # response_message = json.loads(response.data.decode("utf-8"))
        response_message2 = json.loads(response2.data.decode("utf-8"))

        # self.assertEqual(response_message['message'], 'Invalid Token!')
        self.assertEqual(response_message2['message'], 'Token is missing!')

    def test_valid_blacklisted_token_logout(self):
        """ Test for logout after a valid token gets blacklisted  """

        with self.client:
            create_user = {"email": "timgee@email.com",
                           "username": "TimGi",
                           "password": "tim12345"
                           }

            self.client.post("/api/v2/auth/register",
                             data=json.dumps(create_user),
                             content_type="application/json")
            login_response = self.client.post("/api/v2/auth/login",
                                              data=json.dumps(create_user),
                                              content_type="application/json")
            # blacklist a valid token
            blacklist_token = BlacklistToken(
                token=json.loads(login_response.data.decode())['auth_token'])
            db.session.add(blacklist_token)
            db.session.commit()
            # blacklisted valid token logout

            response = self.client.post(
                '/api/v2/auth/businesses',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        login_response.data.decode()
                    )['auth_token']
                ))
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Invalid Token!')
            self.assertEqual(response.status_code, 401)

    def test_reset_password(self):
        with self.client:
            create_user = {"email": "timgee@email.com",
                           "username": "TimGi",
                           "password": "Tim12345."
                           }

            self.client.post("/api/v2/auth/register",
                             data=json.dumps(create_user),
                             content_type="application/json")
            login_response = self.client.post("/api/v2/auth/login",
                                              data=json.dumps(create_user),
                                              content_type="application/json")
            password_reset = {"email": "timgee@email.com",
                              "old_password": "Tim12345.",
                              "new_password": "Tim123456-.",
                              "confirm_password": "Tim123456-."
                              }
            password_reset2 = {"email": "timgee@email.com",
                               "old_password": "Tim12345.",
                               "new_password": "Tim123456",
                               "confirm_password": "Tim123456"
                               }
            reset_response = self.client.put("/api/v2/auth/reset-password",
                                             data=json.dumps(password_reset),
                                             content_type="application/json",
                                             headers=dict(
                                                 Authorization='Bearer ' + json.loads(
                                                     login_response.data.decode()
                                                 )['auth_token']
                                             ))
            reset_response2 = self.client.put("/api/v2/auth/reset-password",
                                              data=json.dumps(password_reset2),
                                              content_type="application/json",
                                              headers=dict(
                                                  Authorization='Bearer ' + json.loads(
                                                      login_response.data.decode()
                                                  )['auth_token']
                                              ))

            data = json.loads(reset_response.data.decode())
            data2 = json.loads(reset_response2.data.decode())

            self.assertEqual(data['message'], 'Password successfully reset.')
            self.assertEqual(data2['msg'], 'Your password should have at least 1 capital letter, '
                                           'special character and number.')
            self.assertEqual(reset_response.status_code, 200)
            self.assertEqual(reset_response.status_code, 200)

    def test_failed_reset_password(self):
        with self.client:
            create_user = {"email": "timgee@email.com",
                           "username": "TimGi",
                           "password": "Tim12345."
                           }

            self.client.post("/api/v2/auth/register",
                             data=json.dumps(create_user),
                             content_type="application/json")
            login_response = self.client.post("/api/v2/auth/login",
                                              data=json.dumps(create_user),
                                              content_type="application/json")
            password_reset = {"email": None,
                              "old_password": "Tim12345.",
                              "new_password": "Tim123456-.",
                              "confirm_password": "Tim123456-."
                              }
            password_reset2 = {"email": "timgee@email.com",
                               "old_password": None,
                               "new_password": "Tim123456-.",
                               "confirm_password": "Tim123456-."
                               }
            password_reset3 = {"email": "timgee@email.com",
                               "old_password": "Tim12345.",
                               "new_password": None,
                               "confirm_password": "Tim123456-."
                               }
            password_reset4 = {"email": "timgee@email.com",
                               "old_password": "Tim12345.",
                               "new_password": "Tim123456-.",
                               "confirm_password": None
                               }
            password_reset5 = {"email": "timgee@email.com",
                               "old_password": "Tim12345.",
                               "new_password": "Tim123456-.",
                               "confirm_password": "Tim123456-.."
                               }
            password_reset6 = {"email": "timgee1@email.com",
                               "old_password": "Tim12345.",
                               "new_password": "Tim123456-.",
                               "confirm_password": "Tim123456-.."
                               }

            reset_response = self.client.put("/api/v2/auth/reset-password",
                                             data=json.dumps(password_reset),
                                             content_type="application/json",
                                             headers=dict(
                                                 Authorization='Bearer ' + json.loads(
                                                     login_response.data.decode()
                                                 )['auth_token']
                                             ))
            reset_response2 = self.client.put("/api/v2/auth/reset-password",
                                              data=json.dumps(password_reset2),
                                              content_type="application/json",
                                              headers=dict(
                                                  Authorization='Bearer ' + json.loads(
                                                      login_response.data.decode()
                                                  )['auth_token']
                                              ))
            reset_response3 = self.client.put("/api/v2/auth/reset-password",
                                              data=json.dumps(password_reset3),
                                              content_type="application/json",
                                              headers=dict(
                                                  Authorization='Bearer ' + json.loads(
                                                      login_response.data.decode()
                                                  )['auth_token']
                                              ))
            reset_response4 = self.client.put("/api/v2/auth/reset-password",
                                              data=json.dumps(password_reset4),
                                              content_type="application/json",
                                              headers=dict(
                                                  Authorization='Bearer ' + json.loads(
                                                      login_response.data.decode()
                                                  )['auth_token']
                                              ))
            reset_response5 = self.client.put("/api/v2/auth/reset-password",
                                              data=json.dumps(password_reset5),
                                              content_type="application/json",
                                              headers=dict(
                                                  Authorization='Bearer ' + json.loads(
                                                      login_response.data.decode()
                                                  )['auth_token']
                                              ))
            reset_response6 = self.client.put("/api/v2/auth/reset-password",
                                              data=json.dumps(password_reset6),
                                              content_type="application/json",
                                              headers=dict(
                                                  Authorization='Bearer ' + json.loads(
                                                      login_response.data.decode()
                                                  )['auth_token']
                                              ))

            data = json.loads(reset_response.data.decode())
            data2 = json.loads(reset_response2.data.decode())
            data3 = json.loads(reset_response3.data.decode())
            data4 = json.loads(reset_response4.data.decode())
            data5 = json.loads(reset_response5.data.decode())
            data6 = json.loads(reset_response6.data.decode())

            self.assertEqual(data['msg'], 'Please enter your email')
            self.assertEqual(data2['msg'], 'Please enter your old password.')
            self.assertEqual(data3['msg'], 'Please enter your new password.')
            self.assertEqual(data4['msg'], 'Please confirm your password.')
            self.assertEqual(data5['message'], 'Passwords do not match.')
            self.assertEqual(data6['message'], 'User not found.')

            self.assertEqual(reset_response.status_code, 401)
            self.assertEqual(reset_response2.status_code, 401)
            self.assertEqual(reset_response3.status_code, 401)
            self.assertEqual(reset_response4.status_code, 401)
            self.assertEqual(reset_response5.status_code, 401)
            self.assertEqual(reset_response6.status_code, 400)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.drop_all()
            db.session.remove()


if __name__ == '__main__':
    unittest.main()
