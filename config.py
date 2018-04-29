import os

# This is a secrete key for session
SECRETE_KEY = os.urandom(24)
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
SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}'.format(DIALECT, DRIVER, USERNAME, PASSWORD, ADDRESS, PORT, DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = False