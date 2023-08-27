import os

basedir = os.path.abspath(os.path.dirname(__file__))

# Google Cloud SQL (change this accordingly)
PASSWORD ="signlingo2023"
PUBLIC_IP_ADDRESS ="34.80.197.140"
PROJECT_ID = "signlingo"
REGION = "asia-east1"  # Replace with your instance's region
INSTANCE_NAME = "user"
DBNAME = 'user_information'


class Config:
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqldb://root:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket=/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = '8927zaaz'

    # Configure Flask-Mail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'signlingo.co@gmail.com'
    MAIL_PASSWORD = 'fmiwnawsvehchgmu'
    MAIL_DEFAULT_SENDER = 'signlingo.co@gmail.com'


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


app_config = DevelopmentConfig
