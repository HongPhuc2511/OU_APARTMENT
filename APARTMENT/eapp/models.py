import datetime
from email.policy import default
from statistics import quantiles

from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from eapp import db, app
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, Date
from eapp.enums import UserRole, ContractType, InvoiceType, PaymentType, PaymentStatus, ContractDuration
from dateutil.relativedelta import relativedelta


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class Address(BaseModel):
    address = Column(String(250), nullable=False)
    country = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)


def __str__(self):
    return self.address


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    phone = Column(String(50), nullable=False, unique=True)
    avatar = Column(String(200),default='https://res.cloudinary.com/dcvwzsnhj/image/upload/v1764126854/1_wuddkf.jpg')
    user_role = Column(Enum(UserRole), default=UserRole.USER)

    address = db.relationship("Address", uselist=False,
                              backref="user", cascade="all, delete-orphan")
    contracts = db.relationship("RentalContract", back_populates="user", lazy=True)

    def __str__(self):
        return self.name


class ApartmentType(BaseModel):
    name = Column(String(50), unique=True)
    apartments = db.relationship('Apartment', back_populates='apartment_type', lazy=True)

    def __str__(self):
        return self.name   # Flask-Admin sẽ hiển thị tên này trong dropdown


class Apartment(BaseModel):
    name = Column(String(50))
    price = Column(Float, default=0)
    area = Column(Float, default=0)
    status = Column(Enum(ContractType, name="contract_type_enum"),
                    default=ContractType.TRONG)
    image = Column(String(200), default="https://res.cloudinary.com/dcvwzsnhj/image/upload/v1764126854/1_wuddkf.jpg")
    type_id = Column(Integer, ForeignKey(ApartmentType.id), nullable=False)

    apartment_type = db.relationship("ApartmentType", back_populates="apartments", lazy=True)

    services = db.relationship("ServiceDetail", backref="apartment", lazy=True,cascade="all, delete-orphan")
    rental_contracts = db.relationship("RentalContract", back_populates="apartment", lazy=True)

    apartment_Rule = db.relationship('ApartmentRule', backref='apartment', lazy=True)

    def __str__(self):
        return self.name

class ApartmentRule(BaseModel):
    rule = Column(String(200), nullable=False)
    apartment_id = Column(Integer, ForeignKey(Apartment.id), nullable=False)


    def __str__(self):
        return self.rule


class ServiceCategory(BaseModel):
    name = Column(String(50), nullable=False)
    description = Column(String(100))
    Services = db.relationship('Service', backref='service_category', lazy=True)

    def __str__(self):
        return self.name


class Service(BaseModel):
    name = Column(String(50), nullable=False)
    unit_price=Column(Float, default=0)
    description = Column(String(100))
    service_type_id = Column(Integer, ForeignKey(ServiceCategory.id), nullable=False)

    apartments = db.relationship("ServiceDetail", backref="service", lazy=True)

    def __str__(self):
        return self.name


class ServiceDetail(BaseModel):
    name = Column(String(50), nullable=False)
    quantity = Column(Float, default=0)
    price = Column(Float, default=0)
    dateuse = Column(Date,default=datetime.date.today())

    service_id = Column(Integer, ForeignKey(Service.id), nullable=False)
    apartment_id = Column(Integer, ForeignKey(Apartment.id), nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'quantity' in kwargs and 'service_id' in kwargs:
            service = db.session.get(Service, kwargs['service_id'])
            if service:
                self.price = kwargs['quantity'] * service.unit_price

    def __str__(self):
        return self.name


class RentalContract(BaseModel):
    start_date = Column(Date)
    end_date = Column(Date)
    price = Column(Float, default=0)
    invoices = db.relationship( 'Invoice', backref='rental_contract', lazy=True, cascade="all, delete-orphan" )
    duration = db.Column(db.Enum(ContractDuration), nullable=False)

    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    apartment_id = Column(Integer, ForeignKey(Apartment.id), nullable=False)

    user = db.relationship("User", back_populates="contracts",lazy=True)
    apartment = db.relationship("Apartment", back_populates="rental_contracts",lazy=True)


    def calculate_end_date(self):
        if self.start_date and self.duration:
            if self.duration == ContractDuration.SIX_MONTHS:
                    self.end_date = self.start_date + relativedelta(months=6)
            elif self.duration == ContractDuration.ONE_YEAR:
                self.end_date = self.start_date + relativedelta(years=1)

    def __str__(self):
        return f"Hợp đồng của {self.user.name} phòng {self.apartment.name}"


class Invoice(BaseModel):
    issue_date = Column(Date)
    due_date = Column(Date)
    amount = Column(Float, nullable=False)
    status = Column(Enum(InvoiceType, name="invoice_enum"), default=InvoiceType.CHUA_THANH_TOAN)
    payments = db.relationship('Payment', backref='invoice', lazy=True)

    contract_id = Column(Integer, ForeignKey(RentalContract.id), nullable=False)

    def __str__(self):
        return str(self.issue_date)


class Payment(BaseModel):
    payment_date = Column(Date)
    amount = Column(Float, default=0)
    method = Column(Enum(PaymentType), name="payment_type_enum", nullable=False)
    status = Column(Enum(PaymentStatus, name="payment_status_enum"), nullable=False)
    note = Column(String(200))

    invoice_id = Column(Integer, ForeignKey(Invoice.id), nullable=False)

    def __str__(self):
        return self.method.name


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        # a = Address(address="123 Main Street", country="VIETNAM")
        #
        # import hashlib
        #
        # u = User(name='Phuc', username='HongPhuc',
        #          password=str(hashlib.md5("123456".encode('utf-8')).hexdigest()),
        #          email='thanhhung332@gmail.com',
        #          phone='0359880036',
        #          user_role=UserRole.USER,
        #          )
        # db.session.add(u)
        # db.session.commit()
        #
        # type1=ApartmentType(name="Căn hộ 1 phòng")
        # type2 = ApartmentType(name="Căn hộ 2 phòng")
        # type3 = ApartmentType(name="Studio")
        # db.session.add_all([type1,type2,type3])
        # db.session.commit()
        #
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
        #
        # r = ApartmentRule(rule='Được phép nuôi thú cưng, không được gây tiếng ồn lớn...', apartment_id=1)
        # db.session.add(r)
        #
        # sc=ServiceCategory(name="Điện,nước",description="Tiền điện và tiền nước")
        # db.session.add(sc)
        # db.session.commit()
        #
        # s=Service(name='Tiền điện',unit_price=4000,description="Tiền điện",service_type_id=1)
        # db.session.add(s)
        # db.session.commit()
        # #
        # se_de=ServiceDetail(name="Tháng 11",quantity=10,dateuse=datetime.date(2025,11,25),service_id=3,apartment_id=1)
        # db.session.add(se_de)
        # db.session.commit()

        # contract=RentalContract(start_date=datetime.date(2025, 11, 25),
        #                          apartment_id=1,user_id=1,duration=ContractDuration.SIX_MONTHS)
        # contract.calculate_end_date()
        # db.session.add(contract)
        # db.session.commit()

        # i=Invoice(issue_date=datetime.date.today(),due_date=datetime.date(2025,12,30),
        #  amount=100,status=InvoiceType.CHUA_THANH_TOAN,contract_id=1)
        # db.session.add(i)
        # db.session.commit()
        #
        # p=Payment(payment_date=datetime.date.today(),amount=2000000,method=PaymentType.TIEN_MAT,
        #           status=PaymentStatus.THANH_CONG,note="Tru 200000",invoice_id=1)
        # db.session.add(p)
        # db.session.commit()
