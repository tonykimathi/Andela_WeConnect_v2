import unittest
import json
from app.models import db
from tests.base_test import BaseTestCase


class BusinessTestCase(BaseTestCase):

    def test_successful_business_registration(self):
        create_user = {"email": "tomgeeF@email.com", "username": "TomGiF", "password": "tim12345"}

        self.client.post("/api/v2/auth/register", data=json.dumps(create_user), content_type="application/json")

        login_response = self.client.post("/api/v2/auth/login", data=json.dumps(create_user),
                                          content_type="application/json")

        create_business = {"business_name": "St. Pius The Tenth", "description": "This is a school founded in 2015",
                           "category": "School", "location": "Meru"}

        business_response = self.client.post("/api/v2/auth/businesses", data=json.dumps(create_business),
                                             content_type="application/json", headers=dict(
                                                 Authorization='Bearer ' + json.loads(login_response.data.decode())
                                                 ['auth_token']))
        data = json.loads(business_response.data.decode())
        self.assertEqual(data['message'], "Business created successfully")
        self.assertEqual(business_response.status_code, 201)

    def test_failed_business_registration(self):
        create_user = {"email": "tomgeeF@email.com", "username": "TomGiF", "password": "tim12345"}

        self.client.post("/api/v2/auth/register", data=json.dumps(create_user), content_type="application/json")

        login_response = self.client.post("/api/v2/auth/login", data=json.dumps(create_user),
                                          content_type="application/json")

        create_business = {"business_name": None, "description": "This is a school founded in 2015",
                           "category": "School", "location": "Meru"}

        create_business2 = {"business_name": "Andela", "description": None, "category": "School", "location": "Meru"}

        create_business3 = {"business_name": "Andela", "description": "This is a school founded in 2015",
                            "category": None, "location": "Meru"}

        create_business4 = {"business_name": "Andela", "description": "This is a school founded in 2015",
                            "category": "School", "location": None}

        business_response = self.client.post("/api/v2/auth/businesses", data=json.dumps(create_business),
                                             content_type="application/json", headers=dict(
                                                 Authorization='Bearer ' + json.loads(login_response.data.decode())
                                                 ['auth_token']))
        business_response2 = self.client.post("/api/v2/auth/businesses", data=json.dumps(create_business2),
                                              content_type="application/json", headers=dict(
                                                  Authorization='Bearer ' + json.loads(login_response.data.decode())
                                                  ['auth_token']))
        business_response3 = self.client.post("/api/v2/auth/businesses", data=json.dumps(create_business3),
                                              content_type="application/json", headers=dict(
                                                  Authorization='Bearer ' + json.loads(login_response.data.decode())
                                                  ['auth_token']))
        business_response4 = self.client.post("/api/v2/auth/businesses", data=json.dumps(create_business4),
                                              content_type="application/json", headers=dict(
                                                  Authorization='Bearer ' + json.loads(login_response.data.decode())
                                                  ['auth_token']))

        data = json.loads(business_response.data.decode())
        data2 = json.loads(business_response2.data.decode())
        data3 = json.loads(business_response3.data.decode())
        data4 = json.loads(business_response4.data.decode())

        self.assertEqual(data['message'], "Please input a business name.")
        self.assertEqual(business_response.status_code, 401)
        self.assertEqual(data2['message'], "Please input a description.")
        self.assertEqual(business_response.status_code, 401)
        self.assertEqual(data3['message'], "Please input a category.")
        self.assertEqual(business_response.status_code, 401)
        self.assertEqual(data4['message'], "Please input a location.")
        self.assertEqual(business_response.status_code, 401)

    def test_successful_business_update(self):
        create_user = {"email": "tomgeeF@email.com", "username": "TomGiF", "password": "tim12345"}
        self.client.post("/api/v2/auth/register", data=json.dumps(create_user), content_type="application/json")

        login_response = self.client.post("/api/v2/auth/login", data=json.dumps(create_user),
                                          content_type="application/json")

        create_business = {"business_name": "St. Pius The Tenth", "description": "This is a school founded in 2015",
                           "category": "School", "location": "Meru", "user_id": 1}

        self.client.post("/api/v2/auth/businesses", data=json.dumps(create_business),
                         content_type="application/json", headers=dict(
                             Authorization='Bearer ' + json.loads(login_response.data.decode())['auth_token']))

        update_business = {"business_name": "St. Pius The Tenth Academy", "description": "This was founded in 2017",
                           "category": "School", "location": "Meru"}
        update_response = self.client.put("/api/v2/auth/businesses/1",
                                          data=json.dumps(update_business), content_type="application/json",
                                          headers=dict(
                                              Authorization='Bearer ' + json.loads(
                                                  login_response.data.decode())['auth_token']))
        fail_update_response = self.client.put("/api/v2/auth/businesses/3", data=json.dumps(update_business),
                                               content_type="application/json", headers=dict(
                                                   Authorization='Bearer ' + json.loads(
                                                       login_response.data.decode())['auth_token']))
        data = json.loads(update_response.data.decode())
        data2 = json.loads(fail_update_response.data.decode())

        self.assertEqual(data['message'], "Business updated successfully")
        self.assertEqual(data2['message'], "Business entered does not exist")

        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(fail_update_response.status_code, 403)

    def test_view_all_businesses(self):
        create_user = {"email": "tomgeeF@email.com", "username": "TomGiF", "password": "tim12345"}
        self.client.post("/api/v2/auth/register", data=json.dumps(create_user), content_type="application/json")

        login_response = self.client.post("/api/v2/auth/login", data=json.dumps(create_user),
                                          content_type="application/json")

        create_business = {"business_name": "St. Pius The Tenth", "description": "This was founded in 2015",
                           "category": "School", "location": "Meru", "user_id": 1}
        create_business2 = {"business_name": "St. Pius The Tenth", "description": "This is a school founded in 2015",
                            "category": "School", "location": "Meru", "user_id": 1}

        self.client.post("/api/v2/auth/businesses", data=json.dumps(create_business),
                         content_type="application/json", headers=dict(
                             Authorization='Bearer ' + json.loads(login_response.data.decode())['auth_token']))
        self.client.post("/api/v2/auth/businesses",
                         data=json.dumps(create_business2), content_type="application/json",
                         headers=dict(
                             Authorization='Bearer ' + json.loads(login_response.data.decode())['auth_token']))
        business_response3 = self.client.get("/api/v2/auth/businesses?location=Meru", content_type="application/json",
                                             headers=dict(
                                                 Authorization='Bearer ' + json.loads(login_response.data.decode())
                                                 ['auth_token']))
        business_response2 = self.client.get("/api/v2/auth/businesses?q=Tenth", content_type="application/json",
                                             headers=dict(
                                                 Authorization='Bearer ' + json.loads(login_response.data.decode())
                                                 ['auth_token']))
        business_response = self.client.get("/api/v2/auth/businesses?category=School",
                                            content_type="application/json",
                                            headers=dict(
                                                Authorization='Bearer ' + json.loads(login_response.data.decode())
                                                ['auth_token']))

        self.assertEqual(business_response.status_code, 200)
        self.assertEqual(business_response2.status_code, 200)
        self.assertEqual(business_response3.status_code, 200)

    def test_view_single_business(self):
        create_user = {"email": "tomgeeF@email.com", "username": "TomGiF", "password": "tim12345"}
        self.client.post("/api/v2/auth/register", data=json.dumps(create_user), content_type="application/json")

        login_response = self.client.post("/api/v2/auth/login", data=json.dumps(create_user),
                                          content_type="application/json")

        create_business = {"business_name": "St. Pius The Tenth", "description": "This is a school founded in 2015",
                           "category": "School", "location": "Meru", "user_id": 1}

        self.client.post("/api/v2/auth/businesses", data=json.dumps(create_business), content_type="application/json",
                         headers=dict(
                             Authorization='Bearer ' + json.loads(login_response.data.decode())['auth_token']))

        business_response = self.client.get("/api/v2/auth/businesses/1", content_type="application/json",
                                            headers=dict(
                                                Authorization='Bearer ' + json.loads(login_response.data.decode())
                                                ['auth_token']))
        self.assertEqual(business_response.status_code, 200)

    def test_delete_business(self):
        create_user = {"email": "tomgeeF@email.com", "username": "TomGiF", "password": "tim12345"}
        self.client.post("/api/v2/auth/register", data=json.dumps(create_user), content_type="application/json")

        login_response = self.client.post("/api/v2/auth/login", data=json.dumps(create_user),
                                          content_type="application/json")

        create_business = {"business_name": "St. Pius The Tenth", "description": "This is a school founded in 2015",
                           "category": "School", "location": "Meru", "user_id": 1}

        self.client.post("/api/v2/auth/businesses", data=json.dumps(create_business),
                         content_type="application/json",
                         headers=dict(
                             Authorization='Bearer ' + json.loads(login_response.data.decode())['auth_token']))

        business_response = self.client.delete("/api/v2/auth/businesses/1", content_type="application/json",
                                               headers=dict(
                                                   Authorization='Bearer ' + json.loads(login_response.data.decode())
                                                   ['auth_token']))
        self.assertEqual(business_response.status_code, 200)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.drop_all()
            db.session.remove()


if __name__ == '__main__':
    unittest.main()
