from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    reset_token = db.Column(db.String(100), nullable=True)
    reset_token_expiration = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return (f"<User(username='{self.username}', email='{self.email}', "
                f"full_name='{self.full_name}', phone_number='{self.phone_number}')>")

    @classmethod
    def check_email_exists(cls, email):
        return cls.query.filter_by(email=email).first() is not None

    @classmethod
    def check_username_exists(cls, username):
        return cls.query.filter_by(username=username).first() is not None