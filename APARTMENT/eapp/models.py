from sqlalchemy.orm import Relationship
from flask_login import UserMixin
from eapp import db,app
from sqlalchemy import  Column, Integer, String,Float,ForeignKey,Enum
from enum import Enum as UserEnum

class UserRole(UserEnum):
    USER=1
    CUSTOMER=2
    ADMIN=3

class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)

class User(BaseModel,UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False,unique=True)
    password = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    phone = Column(String(50), nullable=False, unique=True)
    user_role = Column(Enum(UserRole), default=UserRole.USER)

class ApartmentType(BaseModel):
    name = Column(String(50),unique=True)
    apartments = db.relationship('Apartment', backref='apartment_type', lazy=True)

    def __str__(self):
        return self.name


class Apartment(BaseModel):
    name = Column(String(50))
    price = Column(Float, default=0)
    area = Column(Float, default=0)
    image = Column(String(200), default="https://res.cloudinary.com/dcvwzsnhj/image/upload/v1764126854/1_wuddkf.jpg")
    type_id = Column(Integer, ForeignKey(ApartmentType.id), nullable=False)

    def __str__(self):
        return self.apartment_type.name


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        # import hashlib
        # u=User(name='admin',username='HongPhuc',
        #        password=str(hashlib.md5("123456".encode('utf-8')).hexdigest()),
        #        email='hoanghongphucgl123@gmail.com',
        #        phone='0359880031',
        #        user_role=UserRole.ADMIN)
        # db.session.add(u)
        # db.session.commit()

        # type1=ApartmentType(name="Căn hộ 1 phòng")
        # type2 = ApartmentType(name="Căn hộ 2 phòng")
        # type3 = ApartmentType(name="Studio")
        # db.session.add_all([type1,type2,type3])
        # db.session.commit()

        # apartments = [{
        #     'name':"1PN-001",
        #     'price': 20000,
        #     'area': 40.0,
        #     'image': "https://res.cloudinary.com/dcvwzsnhj/image/upload/v1764126854/1_wuddkf.jpg",
        #     'type_id': "1"
        # }, {
        #     'name': "2PN-001",
        #     'price': 20000,
        #     'area': 40.0,
        #     'image': "https://res.cloudinary.com/dcvwzsnhj/image/upload/v1764126854/1_wuddkf.jpg",
        #     'type_id': "2"
        # }, {
        #     'name': "ST-001",
        #     'price': 20000,
        #     'area': 40.0,
        #     'image': "https://res.cloudinary.com/dcvwzsnhj/image/upload/v1764126854/1_wuddkf.jpg",
        #     'type_id': "3"
        # }, {
        #     'name': "ST-002",
        #     'price': 20000,
        #     'area': 40.0,
        #     'image': "https://res.cloudinary.com/dcvwzsnhj/image/upload/v1764126854/1_wuddkf.jpg",
        #     'type_id': "3"
        # }]
        #
        # for a in apartments:
        #     apa = Apartment(**a)
        #     db.session.add(apa)

        db.session.commit()
