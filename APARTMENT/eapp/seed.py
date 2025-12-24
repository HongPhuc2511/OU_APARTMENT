import random
from datetime import date, timedelta
from eapp import db, app
from eapp.models import Apartment, ApartmentType, User, RentalContract, Invoice, Payment
from eapp.enums import ContractType,UserRole, ContractDuration,InvoiceType, PaymentType, PaymentStatus


def seed_apartments():
    types = [
        ApartmentType(name="Studio1"),
        ApartmentType(name="1 Bedroom"),
        ApartmentType(name="2 Bedroom")
    ]
    db.session.add_all(types)
    db.session.commit()

    statuses = [
        ContractType.TRONG,
        ContractType.DA_DAT_COC,
        ContractType.DANG_THUE
    ]

    apartments = []
    for i in range(1, 31):
        apartments.append(
            Apartment(
                name=f"Phòng {i}",
                price=random.randint(3, 8) * 1_000_000,
                area=random.randint(25, 60),
                status=random.choice(statuses),
                apartment_type=random.choice(types)
            )
        )

    db.session.add_all(apartments)
    db.session.commit()

def seed_users_and_contracts(apartments):
    users = []
    for i in range(1, 11):
        users.append(
            User(
                name=f"Khách {i}",
                username=f"user{i}",
                password="123456",
                email=f"user{i}@gmail.com",
                phone=f"09000000{i}",
                user_role=UserRole.USER
            )
        )
    db.session.add_all(users)
    db.session.commit()

    contracts = []
    for i in range(15):
        start = date.today() - timedelta(days=random.randint(30, 300))
        duration = random.choice(list(ContractDuration))

        contract = RentalContract(
            user=random.choice(users),
            apartment=random.choice(apartments),
            start_date=start,
            duration=duration,
            price=random.randint(3, 8) * 1_000_000
        )
        contract.calculate_end_date()
        contracts.append(contract)

    db.session.add_all(contracts)
    db.session.commit()

def seed_invoices(contracts):
    invoices = []
    for c in contracts:
        for _ in range(random.randint(1, 4)):
            issue = c.start_date + timedelta(days=random.randint(0, 200))
            invoice = Invoice(
                issue_date=issue,
                due_date=issue + timedelta(days=7),
                amount=c.price,
                status=InvoiceType.DA_THANH_TOAN,
                rental_contract=c
            )
            invoices.append(invoice)

    db.session.add_all(invoices)
    db.session.commit()

with app.app_context():
    seed_apartments()
    apartments = Apartment.query.all()
    seed_users_and_contracts(apartments)
    contracts = RentalContract.query.all()
    seed_invoices(contracts)