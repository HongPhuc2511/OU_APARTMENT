from flask import render_template, request, redirect, jsonify, session
from flask_login import login_user, logout_user
from sqlalchemy.testing import emits_warning

from eapp.enums import ContractType
from eapp.models import UserRole, Apartment, ApartmentType
from eapp import app, dao,login,utils
import math

@app.route('/')
def index():

    apartment=dao.load_apartments(

        type_id=request.args.get("apartmenttype_id"),
                                  kw=request.args.get("kw"),
                                  page=request.args.get('page',1))

    return render_template('index.html',
                           pages=math.ceil(dao.count_apartments()/app.config['PAGE_SIZE']),
                           apartment=apartment)

@app.route('/login')
def login_view():
    return render_template('login.html')

@app.route('/register')
def register_view():
    return render_template('register.html')

@app.route('/register',methods=['post'])
def register_process():
    name = request.form.get('name')
    username = request.form.get('username')
    email = request.form.get('email')
    phone = request.form.get('phone')
    password = request.form.get('password')
    confirm = request.form.get('confirm')
    avatar = request.files.get('avatar')

    if password != confirm:
        return render_template('register.html', err_msg="Mật khẩu không khớp!")

    if dao.get_user_by_username(username):
        return render_template('register.html', err_msg="Tên đăng nhập đã tồn tại!")

    if dao.get_user_by_email(email):
        return render_template('register.html', err_msg="Email đã được sử dụng!")

    if dao.get_user_by_phone(phone):
        return render_template('register.html', err_msg="Số điện thoại đã được sử dụng!")

    try:
        dao.add_user(
            name=name,
            username=username,
            email=email,
            phone=phone,
            password=password,
            avatar=avatar
        )
    except Exception as ex:
        return render_template('register.html', err_msg="Không thể đăng ký, vui lòng thử lại!")

    return redirect('/login')


def login_view():
    return render_template('login.html')

@app.route('/login',methods=['get','post'])
def login_process():
    print(request.form)
    username = request.form.get('username')
    password = request.form.get('password')

    u=dao.auth_user(username=username,password=password)

    if u:
        login_user(user=u)
    next=request.args.get('next')
    return redirect(next if next else '/')

@app.route('/apartment/<int:id>')
def apartment_detail(id):
    apartment = Apartment.query.get_or_404(id)
    apartmenttype = ApartmentType.query.all()
    return render_template('apartment_detail.html',
                           apartment=apartment,
                           apartmenttype=apartmenttype)

@app.route('/logout')
def logout_process():
    logout_user()
    return redirect('/login')

@app.route('/api/cart',methods=['post'])
def add_to_cart():
    data = request.json

    cart=session.get('cart')
    if not cart:
        cart={}

    id = str(data.get('id'))
    name = data.get('name')
    area = data.get('area')
    apartment_type = data.get('apartment_type')
    image = data.get('image')
    price = data.get('price')

    if id in cart:
        return jsonify({
            "message": "Căn hộ đã được thêm vào!",
            "total_quantity": utils.count_cart(cart)
        })

    cart[id] = {
        "id": id,
        "name": name,
        "area": area,
        "apartment_type": apartment_type,
        "image": image,
        "price": price,
        "quantity": 1
    }
    session['cart']=cart
    session.modified = True

    return jsonify({
        "message": "Đã thêm vào giỏ hàng!",
        "total_quantity": utils.count_cart(cart)
    })

@app.route('/cart')
def cart_view():
    return render_template('cart.html')

@login.user_loader
def load_user(id):
    return dao.load_user_by_id(id)

@app.context_processor
def common_responses():
    return {
        'apartmenttype':dao.load_apartmenttypes(),
        'cart_stats':utils.count_cart(session.get('cart'))
    }

if __name__ == '__main__':
    from eapp import admin
    app.run(debug=True)
