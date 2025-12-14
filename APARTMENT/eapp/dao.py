import hashlib

from sqlalchemy.sql.functions import user

from eapp.enums import ContractType
from eapp.models import ApartmentType, Apartment,User
from eapp import app, db
import cloudinary.uploader

def load_apartmenttypes():
    return ApartmentType.query.all()

def load_apartments(type_id=None,kw=None,page=1):
    query=Apartment.query

    if kw:
        query=query.filter(Apartment.name.contains(kw))


    if type_id:
        query = query.filter(Apartment.type_id==type_id)

    query = query.filter(Apartment.status == ContractType.TRONG)

    if page:
        page = int(page)
        page_size=app.config.get('PAGE_SIZE',8)
        start=(page-1)*page_size
        query=query.slice(start,start+page_size)

    return query.all()

def count_apartments():
    return Apartment.query.count()

def load_user_by_id(id):
    return User.query.get(id)


def auth_user(username, password):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    return User.query.filter(User.username == username.strip(),
                             User.password == password).first()

def get_user_by_username(username):
    return User.query.filter(User.username == username.strip()).first()

def get_user_by_email(email):
    return User.query.filter(User.email == email.strip()).first()

def get_user_by_phone(phone):
    return User.query.filter(User.phone == phone.strip()).first()


def add_user(name,username,email,phone,password,avatar):
    u=User(name=name,username=username.strip(),email=email,phone=phone,
           password=str(hashlib.md5(password.strip().encode('utf-8')).hexdigest()))

    if avatar:
        res=cloudinary.uploader.upload(avatar)
        u.avatar=res.get('url')

    db.session.add(u)
    db.session.commit()