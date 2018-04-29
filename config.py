import os

# This is a secrete key for session
SECRET_KEY = os.urandom(24)
# Debug mode
DEBUG = True
# The setting for database
DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = '123'
ADDRESS = '127.0.0.1'
PORT = '3306'
DATABASE = 'flask_study'
CHARSET = 'utf8'
SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset={}'.format(DIALECT, DRIVER, USERNAME, PASSWORD, ADDRESS, PORT, DATABASE, CHARSET)

SQLALCHEMY_TRACK_MODIFICATIONS = False