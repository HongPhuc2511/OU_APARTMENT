from flask import render_template,request,redirect
from flask_login import login_user

from eapp.enums import ContractType
from eapp.models import UserRole, Apartment, ApartmentType
from eapp import app, dao,login


@app.route('/')
def index():
    apartmenttype = dao.load_apartmenttypes()

    apartment=dao.load_apartments(type_id=request.args.get("apartmenttype_id"),
                                  kw=request.args.get("kw"),
                                  page=request.args.get("page"))

    return render_template('index.html', apartmenttype=apartmenttype,apartment=apartment)

@app.route('/admin-login',methods=['post'])
def admin_login():
    print(request.form)
    username = request.form.get('username')
    password = request.form.get('password')

    u=dao.auth_user(username=username,password=password,user_role=UserRole.ADMIN)

    if u:
        login_user(user=u)

    return redirect('/admin')

@app.route('/apartment/<int:id>')
def apartment_detail(id):
    apartment = Apartment.query.get_or_404(id)
    apartmenttype = ApartmentType.query.all()
    return render_template('apartment_detail.html',
                           apartment=apartment,
                           apartmenttype=apartmenttype)

@login.user_loader
def load_user(id):
    return dao.load_user_by_id(id)


if __name__ == '__main__':
    from eapp import admin
    app.run(debug=True)
