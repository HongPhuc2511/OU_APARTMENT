import hashlib

from sqlalchemy.sql.functions import user

from eapp.enums import ContractType
from eapp.models import ApartmentType, Apartment,User


def load_apartmenttypes():
    return ApartmentType.query.all()

def load_apartments(type_id=None,kw=None,page=1):
    query=Apartment.query

    if kw:
        query=query.filter(Apartment.name.contains(kw))


    if type_id:
        query = query.filter(Apartment.type_id==type_id)

    query = query.filter(Apartment.status == ContractType.TRONG)

    return query.all()


def load_user_by_id(id):
    return User.query.get(id)


def auth_user(username, password, user_role):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    return User.query.filter(User.username == username.strip(),
                             User.password == password,
                             User.user_role == user_role).first()
