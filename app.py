from flask import Flask, render_template, request, session, redirect, url_for, g
import config
from exts import db
from models import Users, Goods, Goods_class, Cart
import functools

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


# Create a decorator to check log status
def check_login(fun):
    @functools.wraps(fun)
    def wrap(*args, **kwargs):
        user_account = session.get('user_account')
        if user_account:
            return fun(*args, **kwargs)
        else:
            return redirect(url_for('login'))

    return wrap


# Add global variable in Jinja2:
# 1. the user info in the session
# 2. Class names
# 3. All goods
# 4. Total price
@app.context_processor
def check_user():
    user_account = session.get('user_account')
    user = Users.query.filter(Users.account == user_account).first()
    classes = Goods_class.query.filter().all()
    all_goods = Goods.query.filter().all()

    if user:
        user_goods = Cart.query.filter(Cart.user_id == user.id).all()
        total_price = 0
        for good in user_goods:
            total_price += int(good.goods_num) * int(get_good(good.goods_id).good_price)

        return {'user': user, 'admin': user.is_admin, 'classes': classes, 'all_goods': all_goods,
                'total_price': total_price}
    else:
        return {'user': '', 'classes': classes, 'all_goods': all_goods}


@app.route('/', methods=['GET', 'POST'])
@app.route('/index/', methods=['GET', 'POST'])
@app.route('/index/<int:page>', methods=['GET', 'POST'])
def index(page=1):
    if request.method == 'GET':
        goods = Goods.query.filter().paginate(page, config.POSTS_PER_PAGE, False)
        return render_template('index.html', goods=goods)
    elif request.method == 'POST':
        user_account = session.get('user_account')
        if user_account:
            user = Users.query.filter(Users.account == user_account).first()
            user_id = user.id
            good_id = request.form.get('good_id')
            check_exist = Cart.query.filter(Cart.user_id == user_id).filter(Cart.goods_id == good_id).first()
            if check_exist:
                check_exist.goods_num = check_exist.goods_num + 1
                db.session.commit()
            else:
                new_cart = Cart(user_id=user_id, goods_id=good_id, goods_num=1)
                db.session.add(new_cart)
                db.session.commit()
            goods = Goods.query.filter().paginate(page, config.POSTS_PER_PAGE, False)
            return render_template('index.html', goods=goods, status=1, color='success', alert='Add to cart successfully!')
        else:
            return redirect(url_for('login'))

    goods = Goods.query.filter().paginate(page, config.POSTS_PER_PAGE, False)
    return render_template('index.html', goods=goods)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # if you have already loged in, then you needn't login again
    if session.get('user_account'):
        return redirect(url_for('index'))

    if request.method == 'GET':
        return render_template('login.html')
    else:
        account = request.form.get('account')
        password = request.form.get('password')
        checkbox = request.form.get('checkbox')
        user = Users.query.filter(Users.account == account, Users.password == password).first()
        if user:
            session['user_account'] = user.account
            # if the checkbox has been selected, set the efficient day of the cookies is 31 days
            if checkbox:
                session.permanent = True
            return redirect(url_for('index'))
        else:
            status = 0
            return render_template('login.html', status=status)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        name = request.form.get('name').strip()
        account = request.form.get('account').strip()
        password = request.form.get('password').strip()
        repass = request.form.get('repassword').strip()
        address = request.form.get('address').strip()

        # Check whether the name is already in the database
        user1 = Users.query.filter(Users.name == name).first()
        if user1:
            status = 1
            return render_template('register.html', status=status)
        else:
            user2 = Users.query.filter(Users.account == account).first()
            if user2:
                status = 2
                return render_template('register.html', status=status)
            elif password != repass:
                status = 3
                return render_template('register.html', status=status)
            elif (password == '') or (repass == '') or (name == '') or (account == '') or (address == ''):
                status = 4
                return render_template('register.html', status=status)
            else:
                newUser = Users(name=name, account=account, password=password, address=address)
                db.session.add(newUser)
                db.session.commit()
                status = 5
                return render_template('register.html', status=status)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/modifyInfo', methods=['GET', 'POST'])
@check_login
def modifyInfo():
    if request.method == 'GET':
        status = 0
        return render_template('user_page.html', status=status)
    else:
        user_account = session.get('user_account')
        user = Users.query.filter(Users.account == user_account).first()
        way = request.form.get('way')
        if way == 'password':
            password = request.form.get('password').strip()
            password1 = request.form.get('password1').strip()
            password2 = request.form.get('password2').strip()
            if (password == '') or (password1 == '') or (password2 == ''):
                status = 1
                return render_template('user_page.html', status=status, alert='Somthing empty', message='Please input password again!')
            elif user.password != password:
                status = 1
                return render_template('user_page.html', status=status, alert='old password wrong', message='Please input it again!')
            elif password1 != password2:
                status = 1
                return render_template('user_page.html', status=status, alert='passwords doesn\'t match', message='Please input it again!')
            else:
                user.password = password1
                db.session.commit()
                session.clear()
                status = 1
                return render_template('user_page.html', color='success', status=status, alert='Modify seccussfully',
                                       message='Please login again!')
        elif way == 'address':
            address = request.form.get('address').strip()
            if address == '':
                status = 1
                return render_template('user_page.html', status=status, alert='New address is empty', message='Please input it again!')
            else:
                user.address = address
                db.session.commit()
                status = 1
                return render_template('user_page.html', color='success', status=status, alert='Modify address successfully')
        elif way == 'Alia':
            alia = request.form.get('alia')
            alia1 = request.form.get('alia1')
            if (alia == '') or (alia1 == ''):
                status = 1
                return render_template('user_page.html', status=status, alert='Something empty!')
            elif alia != user.name:
                status = 1
                return render_template('user_page.html', status=status, alert='Old name is wrong!!', message='Please input it again.')
            else:
                check_user = Users.query.filter(Users.name == alia1).first()
                # check whether the name has already in the database
                if check_user:
                    status = 1
                    return render_template('user_page.html', status=status, alert='The name already existed!!', message='Please change a name.')
                else:
                    user.name = alia1
                    db.session.commit()
                    status = 1
                    return render_template('user_page.html', status=status, color='success', alert='name modify successfully',
                                           message='Please check it in the user info tab.')
        elif way == 'class':
            selected_good = request.form.get('good_name')
            class_name = request.form.get('good_class')
            # print(selected_good + '   ' + class_name)
            # Firstly, we add a new class if it didn't exist
            check_exist = Goods_class.query.filter(Goods_class.class_name == class_name).first()
            # Then get the data of the selected good
            good = Goods.query.filter(Goods.id == selected_good).first()
            if check_exist:
                class_id = check_exist.class_id
                good.class_id = class_id
                db.session.commit()
            else:
                # Add new class
                new_class = Goods_class(class_name=class_name)
                db.session.add(new_class)
                db.session.commit()
                # Modify the good's class
                good.class_id = Goods_class.query.filter(Goods_class.class_name == class_name).first().class_id
                db.session.commit()
            return render_template('user_page.html', status=1, color='success', alert='Add class successfully。')
        elif way == 'add_good':
            good_name = request.form.get('good_name')
            good_desc = request.form.get('good_desc')
            good_price = request.form.get('good_price')
            picture_url = request.form.get('picture_url')
            new_good = Goods(good_name=good_name, good_desc=good_desc, good_price=good_price, picture_url=picture_url)
            db.session.add(new_good)
            db.session.commit()
            return render_template('user_page.html', status=1, color='success', alert='Add good successfully。')


@app.route('/search/', methods=['POST', 'GET'])
@app.route('/search/<search_strin>/', methods=['POST', 'GET'])
@app.route('/search/<search_str>/<int:page>', methods=['POST', 'GET'])
def search(page=1, search_strin=''):
    way = request.form.get('way')
    search_str = request.form.get('search')
    if way == 'add':
        user_account = session.get('user_account')
        if user_account:
            user = Users.query.filter(Users.account == user_account).first()
            user_id = user.id
            good_id = request.form.get('good_id')
            check_exist = Cart.query.filter(Cart.user_id == user_id).filter(Cart.goods_id == good_id).first()
            if check_exist:
                check_exist.goods_num = check_exist.goods_num + 1
                db.session.commit()
            else:
                new_cart = Cart(user_id=user_id, goods_id=good_id, goods_num=1)
                db.session.add(new_cart)
                db.session.commit()
            search_goods = Goods.query.filter(Goods.good_name.like('%''%')).paginate(page, 6,
                                                                                                     False)
            return render_template('search.html', search_goods=search_goods, search_string=search_str, status=1,
                                   color='success', alert='Add to cart successfully!')
        else:
            return redirect(url_for('login'))

    else:
        search_goods = Goods.query.filter(Goods.good_name.like('%' + search_str + '%')).paginate(page, 6,
                                                                                                 False)
        return render_template('search.html', search_goods=search_goods, search_string=search_str)


@app.route('/class/<name>/', methods=['GET', 'POST'])
@app.route('/class/<name>/<int:page>/', methods=['GET', 'POST'])
def class_page(name, page=1):
    if request.method == 'GET':
        # firstly, get the class id
        class_id = Goods_class.query.filter(Goods_class.class_name == name).first().class_id
        # Then, select * from goods where class_id = class_id
        class_goods = Goods.query.filter(Goods.class_id == class_id).paginate(page, 6, False)
        return render_template('class_page.html', class_goods=class_goods, class_name=name)
    elif request.method == 'POST':
        user_account = session.get('user_account')
        if user_account:
            user = Users.query.filter(Users.account == user_account).first()
            user_id = user.id
            good_id = request.form.get('good_id')
            check_exist = Cart.query.filter(Cart.user_id == user_id).filter(Cart.goods_id == good_id).first()
            if check_exist:
                check_exist.goods_num = check_exist.goods_num + 1
                db.session.commit()
            else:
                new_cart = Cart(user_id=user_id, goods_id=good_id, goods_num=1)
                db.session.add(new_cart)
                db.session.commit()
            goods = Goods.query.filter().paginate(page, config.POSTS_PER_PAGE, False)

            class_id = Goods_class.query.filter(Goods_class.class_name == name).first().class_id
            class_goods = Goods.query.filter(Goods.class_id == class_id).paginate(page, 6, False)
            return render_template('class_page.html', class_goods=class_goods, class_name=name, status=1,
                                   color='success', alert='Add to cart successfully!')
        else:
            return redirect(url_for('login'))


@app.route('/cart/', methods=['POST', 'GET'])
@check_login
def cart():
    if request.method == 'GET':
        user_account = session.get('user_account')
        user_id = Users.query.filter(Users.account == user_account).first().id
        user_goods = Cart.query.filter(Cart.user_id == user_id).all()
        return render_template('cart.html', user_goods=user_goods)
    elif request.method == 'POST':
        user_account = session.get('user_account')
        user_id = Users.query.filter(Users.account == user_account).first().id
        good_id = request.form.get('good_id')
        way = request.form.get('way')
        if way == 'delete':
            delete_good = Cart.query.filter(Cart.user_id == user_id).filter(Cart.goods_id == good_id).first()
            db.session.delete(delete_good)
            db.session.commit()
            user_goods = Cart.query.filter(Cart.user_id == user_id).all()
            return render_template('cart.html', user_goods=user_goods)
        if way == 'minus':
            minus_good = Cart.query.filter(Cart.user_id == user_id).filter(Cart.goods_id == good_id).first()
            if minus_good.goods_num > 0:
                minus_good.goods_num = minus_good.goods_num - 1
                db.session.commit()
            user_goods = Cart.query.filter(Cart.user_id == user_id).all()
            return render_template('cart.html', user_goods=user_goods)
        if way == 'plus':
            plus_good = Cart.query.filter(Cart.user_id == user_id).filter(Cart.goods_id == good_id).first()
            plus_good.goods_num = plus_good.goods_num + 1
            db.session.commit()
            user_goods = Cart.query.filter(Cart.user_id == user_id).all()
            return render_template('cart.html', user_goods=user_goods)
        if way == 'pay':
            user_goods = Cart.query.filter(Cart.user_id == user_id).all()
            for good in user_goods:
                db.session.delete(good)
                db.session.commit()
            return render_template('cart.html', status='1', color='success', alert='Successfully paid all things。')


# add a self filter to get goods from goods id
@app.template_filter('get_good_from_id')
def get_good(good_id):
    return Goods.query.filter(Goods.id == good_id).first()


if __name__ == '__main__':
    app.run()
