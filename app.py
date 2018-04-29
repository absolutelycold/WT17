from flask import Flask, render_template, request, session, redirect, url_for, g
import config
from exts import db
from models import Users
import functools

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


# Create a deractor to check log status
def check_login(fun):
    @functools.wraps(fun)
    def wrap(*args, **kwargs):
        user_account = session.get('user_account')
        if user_account:
            return fun(*args, **kwargs)
        else:
            return redirect(url_for('login'))

    return wrap


# 从session中取出登录信息, 并设置为上下文变量
@app.context_processor
def check_user():
    user_account = session.get('user_account')
    user = Users.query.filter(Users.account == user_account).first()
    if user:
        return {'user': user}
    else:
        return {'user': ''}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # 如果登录过了, 就不可以再次登录
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
            # 如果checkbox被选中, 设置session的cookies有效期为31天
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

        # 检查重名
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
                return render_template('user_page.html', status=status, alert='请勿留空', message='请再次输入密码!')
            elif user.password != password:
                status = 1
                return render_template('user_page.html', status=status, alert='原密码输入错误', message='请再次输入密码!')
            elif password1 != password2:
                status = 1
                return render_template('user_page.html', status=status, alert='两次密码不一致', message='请再重新输入!')
            else:
                user.password = password1
                db.session.commit()
                session.clear()
                status = 1
                return render_template('user_page.html', color='success', status=status, alert='成功修改密码',
                                       message='请重新登录!')
        elif way == 'address':
            address = request.form.get('address').strip()
            if address == '':
                status = 1
                return render_template('user_page.html', status=status, alert='新地址为空', message='请重新输入!')
            else:
                user.address = address
                db.session.commit()
                status = 1
                return render_template('user_page.html', color='success', status=status, alert='修改地址成功')
        elif way == 'Alia':
            alia = request.form.get('alia')
            alia1 = request.form.get('alia1')
            if (alia == '') or (alia1 == ''):
                status = 1
                return render_template('user_page.html', status=status, alert='请勿留空!')
            elif alia != user.name:
                status = 1
                return render_template('user_page.html', status=status, alert='原昵称输入错误!!', message='请再次输入.')
            else:
                check_user = Users.query.filter(Users.name == alia1).first()
                # 检查user表中是否已经存在名字是新名字的用户
                if check_user:
                    status = 1
                    return render_template('user_page.html', status=status, alert='此用户名已存在!!', message='请换一个用户名再次输入.')
                else:
                    user.name = alia1
                    db.session.commit()
                    status = 1
                    return render_template('user_page.html', status=status, color='success', alert='修改昵称成功',
                                           message='请殿下查阅.')


if __name__ == '__main__':
    app.run()
