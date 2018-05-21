from app import db


class User(db.Model):

    """

    Creates a User table

    """
    __tablename__ = 'Users'

    user_id = db.Column(db.String(120), primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    password = db.Column(db.String(128))

    def __init__(self, user_id, email, username, password):
        self.user_id = user_id
        self.email = email
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User {}'.format(self.username)


class Business(db.Model):

    """

    Creates a Business table

    """
    __tablename__ = 'Businesses'

    business_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True, unique=True)
    business_name = db.Column(db.String(60), index=True, unique=True)
    description = db.Column(db.String(128))
    location = db.Column(db.String(60), index=True, unique=True)
    category = db.Column(db.String(60), index=True, unique=True)

    def __init__(self, business_id, user_id, business_name, description, location, category):
        self.business_id = business_id
        self.user_id = user_id
        self.business_name = business_name
        self.description = description
        self.location = location
        self.category = category

    def __repr__(self):
        return '<Business {}'.format(self.business_name)


class Review(db.Model):
    """

    Creates a Review table

    """
    __tablename__ = 'Reviews'

    review_id = db.Column(db.Integer, primary_key=True)
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
