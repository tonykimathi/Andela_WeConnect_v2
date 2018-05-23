from app import db
import datetime
import jwt


class User(db.Model):

    """

    Creates a User table

    """
    __tablename__ = 'Users'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # user_id = db.Column(db.String(120), primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    password = db.Column(db.String(128))
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, username, password, admin=False):
        # self.user_id = user_id
        self.email = email
        self.username = username
        self.password = password
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        SECRET_KEY = 'BetterKeepThisSecret'

        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=30),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
            Decodes the auth token
            :param auth_token:
            :return: integer|string
        """

        SECRET_KEY = 'BetterKeepThisSecret'

        try:
            payload = jwt.decode(auth_token, SECRET_KEY,  leeway=10)
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)

            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']

        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def __repr__(self):
        return '<User {}'.format(self.username)


class Business(db.Model):

    """

    Creates a Business table

    """
    __tablename__ = 'Businesses'

    business_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, index=True, unique=True)
    business_name = db.Column(db.String(60), index=True, unique=True)
    description = db.Column(db.String(128))
    location = db.Column(db.String(60), index=True, unique=True)
    category = db.Column(db.String(60), index=True, unique=True)
    created_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, business_name, description, location, category):
        # self.user_id = user_id
        self.business_name = business_name
        self.description = description
        self.location = location
        self.category = category
        self.created_on = datetime.datetime.now()

    def __repr__(self):
        return '<Business {}'.format(self.business_name)


class Review(db.Model):
    """

    Creates a Review table

    """
    __tablename__ = 'Reviews'

    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    business_id = db.Column(db.Integer, index=True, unique=True)
    review_name = db.Column(db.String(60), index=True, unique=True)
    body = db.Column(db.String(128))

    def __init__(self, review_id, business_id, review_name, body):
        self.review_id = review_id
        self.business_id = business_id
        self.review_name = review_name
        self.body = body

    def __repr__(self):
        return '<Review {}'.format(self.review_name)


class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'Blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False

    def __repr__(self):
        return '<id: token: {}'.format(self.token)
