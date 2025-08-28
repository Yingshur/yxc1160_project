import os
import pymysql
from dotenv import load_dotenv

pymysql.install_as_MySQLdb()
load_dotenv()
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
basedir = os.path.abspath(os.path.dirname(__file__))
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'WR#&f&+%78er0we=%799eww+#7^90-;s'

    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'data', 'uploads')
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024
    SQLALCHEMY_DATABASE_URI = ("mysql+pymysql://avnadmin:AVNS_ZtThNkudDKdZCTn-5Q5"
                               "@mysql-1ade3b12-chenyingshu1234-4999.e.aivencloud.com:18443/defaultdb"
                               "?ssl_ca="+ os.path.join(basedir, "app", "static", "ca.pem"))

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

