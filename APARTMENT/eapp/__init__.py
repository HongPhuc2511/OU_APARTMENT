from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app=Flask(__name__)

app.secret_key='ABCDENADA@#%^@##@&#^WSF'
app.config["SQLALCHEMY_DATABASE_URI"] ="mysql+pymysql://root:root@localhost/apartmentdb?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

login = LoginManager(app=app)
db = SQLAlchemy(app=app)