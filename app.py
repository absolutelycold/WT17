from flask import Flask, render_template, request
import config
from exts import db
from models import Users

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        name = request.form.get('name').strip()
        account = request.form.get('account').strip()
        password = request.form.get('password').strip()
        repass = request.form.get('repassword').strip()

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
            elif (password == '') or (repass == '') or (name == '') or (account == ''):
                status = 4
                return render_template('register.html', status=status)
            else:
                newUser = Users(name=name, account=account, password=password)
                db.session.add(newUser)
                db.session.commit()
                status = 5
                return render_template('register.html', status=status)


if __name__ == '__main__':
    app.run()
