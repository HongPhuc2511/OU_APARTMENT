from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary

app=Flask(__name__)

app.secret_key='ABCDENADA@#%^@##@&#^WSF'
app.config["SQLALCHEMY_DATABASE_URI"] ="mysql+pymysql://root:root@localhost/apartmentdb?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 8

login = LoginManager(app=app)
db = SQLAlchemy(app=app)

cloudinary.config(
    cloud_name="dcvwzsnhj",
    api_key="289546862684389",
    api_secret="6iSIGcl5Y3DUDavEIPLEbhPi2vQ"
)
