from ensurepip import bootstrap
from tempfile import template

from dateutil.relativedelta import relativedelta
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla.fields import QuerySelectField
from werkzeug.routing import Rule

from eapp.enums import ContractType, PaymentStatus, InvoiceType
from eapp.models import ApartmentType, Apartment, UserRole, ApartmentRule, RentalContract, Invoice,Payment, Service, \
    ServiceDetail
from flask import template_rendered, jsonify
from flask_admin import Admin
from eapp import db,app
from flask_login import logout_user, current_user
from flask import redirect
from enums import ContractDuration
import dao
from datetime import date

admin=Admin(app=app,name="Apartment Admin")

class AuthenticatedModelView(ModelView):
    def is_accessible(self)->bool:
        return current_user.is_authenticated and current_user.user_role==UserRole.ADMIN

class ApartmentView(AuthenticatedModelView):
    can_export = True
    column_list = ['id','name','price','area','status','apartment_type']
    column_filters = ['price', 'area','status','apartment_type']
    column_searchable_list = ['name']
    edit_modal = True
    page_size = 8

    column_labels = {
        'name': 'Tên căn hộ',
        'price': 'Giá thuê (VNĐ)',
        'area': 'Diện tích (m²)',
        'image': 'Ảnh',
        'status': 'Trạng thái',
        'apartment_type': 'Loại căn hộ',
        'apartment_Rule':'Quy định',
        'services':'Dịch vụ',
        'rental_contracts':'Hợp đồng'
    }

    form_columns = ['name', 'price', 'area', 'status','image','apartment_type','apartment_Rule', 'services', 'rental_contracts']


class ApartmentTypeView(AuthenticatedModelView):
    column_list = ['id','name']
    column_filters = ['name']
    column_labels = {
        'name':'Loại căn hộ'
    }
    form_columns = ['name']
    form_labels = {
        'name': 'Loại căn hộ'
    }
    column_searchable_list = ['name']
    edit_modal = True
    page_size = 8

class Logout_View(BaseView):
    @expose('/')
    def index(self):
        logout_user()

        return redirect('/admin')
    def is_accessible(self)->bool:
        return current_user.is_authenticated

class RuleView(AuthenticatedModelView):
    column_list = ['id','rule']
    column_filters = ['rule']
    column_labels = {
        'rule': 'Quy định'
    }
    edit_modal = True

def get_available_apartments():
    return Apartment.query.filter(Apartment.status == ContractType.TRONG).all()

class ContractView(AuthenticatedModelView):

    column_list = ['id', 'start_date', 'end_date', 'price','duration','user', 'apartment']
    column_filters = ['start_date', 'end_date', 'price', 'apartment_id']
    column_labels = {
        'id': 'Mã hợp đồng',
        'start_date': 'Ngày bắt đầu',
        'duration':'Thời hạn',
        'end_date': 'Ngày kết thúc',
        'price': 'Giá thuê',
        'user': 'Người thuê',
        'apartment': 'Căn hộ'
    }
    form_columns = ['user', 'apartment','start_date','duration','end_date', 'price']

    form_overrides = {
        'apartment': QuerySelectField
    }
    extra_js = [
        '/static/js/contract.js'
    ]

    form_args = {
        'apartment': {
            'query_factory': get_available_apartments,
            'allow_blank': False,
            'label': 'Căn hộ'
        }
    }

    edit_modal = True
    page_size = 8
    column_searchable_list = ['price']
    can_export = True

    form_excluded_columns = ['invoices']

    def calculate_end(self, model):
        if model.start_date and model.duration:
            if model.duration == ContractDuration.SIX_MONTHS:
                model.end_date = model.start_date + relativedelta(months=6)
            elif model.duration == ContractDuration.ONE_YEAR:
                model.end_date = model.start_date + relativedelta(years=1)

    def create_model(self, form):
        model = super().create_model(form)

        self.calculate_end(model)

        if model.apartment:
            model.apartment.status = ContractType.DANG_THUE

        db.session.commit()
        return model

    def update_model(self, form, model):
        super().update_model(form, model)

        self.calculate_end(model)

        if model.apartment:
            model.apartment.status = ContractType.DANG_THUE

        db.session.commit()
        return model

    def on_model_delete(self, model):

        if model.apartment:
            model.apartment.status = ContractType.TRONG

        return super().on_model_delete(model)



class InvoiceView(AuthenticatedModelView):
    column_list = ['id','issue_date','due_date','amount','status','rental_contract']
    column_filters = ['contract_id']
    edit_modal = True
    column_searchable_list = ['issue_date','due_date']
    can_export = True
    column_labels = {
        'id': 'Mã hóa đơn',
        'issue_date': 'Ngày lập',
        'due_date': 'Hạn thanh toán',
        'amount': 'Số tiền',
        'status': 'Trạng thái',
        'rental_contract': 'Hợp đồng thuê',
    }
    form_excluded_columns = ['payments']


class ServiceView(AuthenticatedModelView):
    column_list =['id','name','unit_price','service_type_id']
    column_filters = ['name','service_type_id']
    edit_modal = True
    column_searchable_list = ['name']
    column_labels = {
        'name':'Tên dịch vụ',
        'unit_price':'Giá tiền',
        'description':'Mô tả',
        'service_category':'Loại dịch vụ',
    }
    form_excluded_columns = ['apartments']


class StatsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html',status_apartments=dao.get_apartments_status_stats()
                                                      ,revenue_month=dao.get_revenue_by_month()
                                                      ,contracts_expiring=dao.get_contracts_expiring(90),today=date.today())

    def is_accessible(self) -> bool:
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class PaymentConfirm(BaseView):

    @expose('/')
    def index(self):
        payments = Payment.query.filter_by(
            status=PaymentStatus.CHO_XU_LY
        ).all()
        return self.render('admin/confirm.html', payments=payments)

    @expose('/<int:id>/approve', methods=['POST'])
    def approve(self, id):
        payment = Payment.query.get_or_404(id)

        if payment.status != PaymentStatus.CHO_XU_LY:
            return jsonify({'error': 'Invalid state'}), 400

        payment.status = PaymentStatus.THANH_CONG
        payment.invoice.status = InvoiceType.DA_THANH_TOAN
        payment.invoice.rental_contract.apartment.status = ContractType.DANG_THUE

        db.session.commit()
        return jsonify({'status': 'ok'})

    @expose('/<int:id>/reject', methods=['POST'])
    def reject(self, id):
        payment = Payment.query.get_or_404(id)
        payment.status = PaymentStatus.THAT_BAI

        db.session.commit()
        return jsonify({'status': 'rejected'})

    def is_accessible(self):
        return (
            current_user.is_authenticated and
            current_user.user_role == UserRole.ADMIN
        )


admin.add_view(ApartmentTypeView(ApartmentType,db.session,name='Loại căn hộ'))
admin.add_view(ApartmentView(Apartment,db.session,name='Quản lí căn hộ'))
admin.add_view(ContractView(RentalContract,db.session,name='Quản lí hợp đồng'))
admin.add_view(InvoiceView(Invoice,db.session,name='Quản lí hóa đơn'))
admin.add_view(ServiceView(Service,db.session,name='Quản lí dịch vụ'))
admin.add_view(PaymentConfirm(name="Duyệt thanh toán"))
admin.add_view(StatsView(name='Thống kê & Báo cáo'))
admin.add_view(RuleView(ApartmentRule,db.session,name='Thay đổi quy định'))
admin.add_view(Logout_View(name='Đăng xuất'))