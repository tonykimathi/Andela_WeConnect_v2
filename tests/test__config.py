import unittest
from app import create_app


class TestDevelopmentConfig(unittest.TestCase):

    def test_app_is_development(self):
        app = create_app(config_name='development')
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(app is None)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == 'postgresql://timothy:timmutai@localhost:5432/andela_weconnect'
        )


class TestTestingConfig(unittest.TestCase):

    def test_app_is_testing(self):
        app = create_app(config_name='testing')
        self.assertTrue(app.config['DEBUG'] is False)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == 'postgresql://timothy:timmutai@localhost:5432/test_db'
        )
