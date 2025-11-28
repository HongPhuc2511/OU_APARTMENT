from ensurepip import bootstrap
from tempfile import template

from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose

from eapp.models import ApartmentType, Apartment, UserRole
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
    column_list = ['id','name','price','area','type_id']
    column_filters = ['price', 'area', 'type_id']
    column_searchable_list = ['name']
    edit_modal = True
    page_size = 8
    column_labels = {
        'name': 'Tên căn hộ',
        'price': 'Giá thuê (VNĐ)',
        'area': 'Diện tích (m²)',
        'type_id': 'Loại căn hộ'
    }

class ApartmentTypeView(AuthenticatedModelView):
    column_list = ['id','name']
    column_filters = ['name']
    column_labels = {
        'name':'Loại căn hộ'
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


admin.add_view(ApartmentTypeView(ApartmentType,db.session))
admin.add_view(ApartmentView(Apartment,db.session))
admin.add_view(Logout_View(name='Đăng xuất'))