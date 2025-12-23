
import hashlib


from flask_login import current_user

from eapp.enums import ContractType, ContractDuration, InvoiceType, PaymentType, PaymentStatus
from eapp.models import ApartmentType, Apartment, User, RentalContract, Invoice, Payment
from eapp import app, db
import cloudinary.uploader
from sqlalchemy import func, extract
import datetime

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

def add_contract(cart, payment_method):
    if not cart:
        return


    method_map = {
        'cash': PaymentType.TIEN_MAT,
        'bank': PaymentType.CHUYEN_KHOAN,
        'momo': PaymentType.MOMO,
        'zaloPay': PaymentType.ZALO_PAY
    }

    method = method_map.get(payment_method)
    if not method:
        raise ValueError(f'Invalid payment method: {payment_method}')

    for c in cart.values():
        # 1. Tạo hợp đồng (CHƯA kích hoạt)
        contract = RentalContract(
            user_id=current_user.id,
            apartment_id=c['id'],
            start_date=datetime.date.today(),
            duration=ContractDuration.ONE_YEAR,
            price=c['price']
        )
        contract.calculate_end_date()
        db.session.add(contract)
        db.session.flush()

        invoice = Invoice(
            issue_date=datetime.date.today(),
            due_date=datetime.date.today() + datetime.timedelta(days=7),
            amount=c['price'],
            status=InvoiceType.CHUA_THANH_TOAN,
            contract_id=contract.id
        )
        db.session.add(invoice)
        db.session.flush()


        payment = Payment(
            payment_date=datetime.date.today(),
            amount=c['price'],
            method=method,
            status=PaymentStatus.CHO_XU_LY,
            invoice_id=invoice.id,
            note="User yêu cầu thanh toán"
        )
        db.session.add(payment)

    db.session.commit()


def get_user_contracts(user_id):
    contracts = (db.session.query(RentalContract)
                 .filter_by(user_id=user_id)
                 .order_by(RentalContract.start_date.desc())  # mới nhất trước
                 .all())
    return contracts

def get_apartments_status_stats():
    return (db.session.query(Apartment.status,func.count(Apartment.id)).group_by(Apartment.status).all())

def get_revenue_by_month(year=2025):
    return (
        db.session.query(
            extract('month', Invoice.issue_date).label('month'),
            func.sum(Invoice.amount).label('revenue')
        )
        .filter(
            extract('year', Invoice.issue_date) == year,
            Invoice.status == InvoiceType.DA_THANH_TOAN
        )
        .group_by('month')
        .order_by('month')
        .all()
    )

from datetime import date, timedelta

def get_contracts_expiring(days):
    deadline = date.today() + timedelta(days=days)

    return (
        db.session.query(RentalContract).filter(RentalContract.end_date != None,
                                                RentalContract.end_date >= date.today(),
                                                RentalContract.end_date <= deadline
                                                ).order_by(RentalContract.end_date.asc()).all())
