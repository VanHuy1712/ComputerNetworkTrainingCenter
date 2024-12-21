from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary

app = Flask(__name__)
app.secret_key = '^%^&%^(*^^^&&*^(*^^&$%&*&*%^&$&^'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/trainingcenterdb?charset=utf8mb4" % quote('Admin@123')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 8


db = SQLAlchemy(app)
login = LoginManager(app)

cloudinary.config(cloud_name='dn0kj5rfm',
                  api_key='636627396695933',
                  api_secret='NTSuTm07I86Aj1cMGaZW2cPDMg8')
