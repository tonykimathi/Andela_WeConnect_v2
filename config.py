import os
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = 'postgresql://timothy:timmutai@localhost:5432/andela_weconnect'


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    TEST_DATABASE_URI = os.getenv("TEST_DATABASE_URI")
    # SQLALCHEMY_DATABASE_URI = 'postgresql://timothy:timmutai@localhost:5432/test_db'


class StagingConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig
}
