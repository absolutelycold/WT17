import os

SQLALCHEMY_TRACK_MODIFICATIONS = False

POSTS_PER_PAGE = 6

# This is a secrete key for session
SECRET_KEY = os.urandom(24)
# Debug mode
DEBUG = True
# The setting for database
DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'l630003036'
PASSWORD = 'student'
ADDRESS = '172.16.199.70'
PORT = '3306'
DATABASE = 'l630003036'
CHARSET = 'utf8'
SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset={}'.format(DIALECT, DRIVER, USERNAME, PASSWORD, ADDRESS, PORT, DATABASE, CHARSET)

