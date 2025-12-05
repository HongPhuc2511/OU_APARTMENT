from ensurepip import bootstrap
from tempfile import template

from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from werkzeug.routing import Rule

from eapp.models import ApartmentType, Apartment, UserRole, ApartmentRule, RentalContract,Invoice
from flask import template_rendered
from flask_admin import Admin
from eapp import db,app
from flask_login import logout_user, current_user
from flask import redirect

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
        'status': 'Trạng thái',
        'apartment_type': 'Loại căn hộ',

    }

    form_columns = ['name', 'price', 'area', 'status', 'apartment_type','apartment_Rule', 'services', 'rentalcontracts']
    form_labels = {
        'name': 'Tên căn hộ',
        'price': 'Giá thuê (VNĐ)',
        'area': 'Diện tích (m²)',
        'status': 'Trạng thái',
        'apartment_type': 'Loại căn hộ',
        'apartment_Rule': 'Quy định',
        'services': 'Dịch vụ',
        'rentalcontracts': 'Hợp đồng'
    }


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

class ContractView(AuthenticatedModelView):
    column_list = ['id', 'start_date', 'end_date', 'price','invoices' 'user_id', 'apartment_id']
    column_filters = ['start_date', 'end_date', 'price', 'apartment_id']
    column_labels = {
        'id': 'Mã hợp đồng',
        'start_date': 'Ngày bắt đầu',
        'end_date': 'Ngày kết thúc',
        'price': 'Giá thuê',
        'invoices':'Hóa đơn',
        'user_id': 'Người thuê',
        'apartment_id': 'Căn hộ'
    }
    form_labels = {
        'start_date': 'Ngày bắt đầu',
        'end_date': 'Ngày kết thúc',
        'price': 'Giá thuê',
        'invoices':'Hóa đơn',
        'user_id': 'Người thuê',
        'apartment_id': 'Căn hộ'
    }
    edit_modal = True
    page_size = 8
    column_searchable_list = ['price']
    can_export = True

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
        'contract_id': 'Hợp đồng thuê',
        'rental_contract': 'Hợp đồng thuê',
        'payments':'Loại thanh toán'
    }

    # form_columns = ['issue_date', 'due_date', 'amount', 'status', 'rental_contract']
    # form_labels = {
    #     'issue_date': 'Ngày lập',
    #     'due_date': 'Hạn thanh toán',
    #     'amount': 'Số tiền',
    #     'status': 'Trạng thái',
    #     'rental_contract': 'Hợp đồng thuê'
    # }

admin.add_view(ApartmentTypeView(ApartmentType,db.session,name='Loại căn hộ'))
admin.add_view(ApartmentView(Apartment,db.session,name='Quản lí căn hộ'))
admin.add_view(ContractView(RentalContract,db.session,name='Quản lí hợp đồng'))
admin.add_view(InvoiceView(Invoice,db.session,name='Quản lí hóa đơn'))
admin.add_view(RuleView(ApartmentRule,db.session,name='Thay đổi quy định'))
admin.add_view(Logout_View(name='Đăng xuất'))