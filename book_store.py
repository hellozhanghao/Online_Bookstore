from flask import Flask, url_for, request, json, jsonify, render_template
import flask_login

from flask import redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:zhanghao@localhost/book_store'
db = SQLAlchemy(app)


# DB schemas
class DB_User(db.Model):
    __tablename__ = 'User'
    username = db.Column('username', db.CHAR(20), primary_key=True)
    password = db.Column('password', db.CHAR(20))
    credit_card = db.Column('credit_card', db.CHAR(20))
    address = db.Column('address', db.CHAR(20))
    phone = db.Column('phone', db.CHAR(20))
    admin = db.Column('admin', db.BOOLEAN)

    def __init__(self, username, password, credit_card, address, phone, admin):
        self.username = username
        self.password = password
        self.credit_card = credit_card
        self.address = address
        self.phone = phone
        self.admin = admin

class DB_Book(db.Model):
    __tablename__ = "Book"
    ISBN = db.Column('ISBN', db.CHAR(14), primary_key=True)
    title = db.Column('title', db.CHAR(40))
    author = db.Column('author', db.CHAR(40))
    publisher = db.Column('publisher', db.CHAR(40))
    year = db.Column('year', db.INTEGER)
    copy = db.Column('copy', db.INTEGER)
    price = db.Column('price', db.FLOAT)
    format = db.Column('format', db.CHAR(20))
    subject = db.Column('subject', db.CHAR(20))
    keywords = db.Column('keywords', db.CHAR(100))


db.create_all()
db.session.commit()

user= DB_User.query.filter_by(username='zhanghao').first()
print(user.admin)



# Example insert
# user=DB_User('someone','password')
# db.session.add(user)
# db.session.commit()

# Example update
# update_this = DB_User.query.filter_by(username='zhanghao').first()
# update_this.password = 'updated'
# db.session.commit()

# Example delete
# delete_this = DB_User.query.filter_by(username='zhanghao').first()
# db.session.delete(delete_this)
# db.session.commit()




# class Person(db.Model):
#     id = db.Column(db.Integer, primary_key= True)
#     name = db.Column(db.String(20))
#     pets = db.relationship('Pet', backref= 'owner', lazy = 'dynamic')
#
#
# class Pet(db.Model):
#     id = db.Column(db.Integer, primary_key= True)
#     name = db.Column(db.String(20))
#     owner_id = db.Column(db.Integer, db.ForeignKey('person.id'))


# db.create_all()
# db.session.commit()


# person_one = Person(name='Anthony')
# person_two = Person(name='Cindy')
# db.session.add(person_one)
# db.session.add(person_two)
# db.session.commit()
#
#
# pet_one = Pet(name ='Spot', owner=person_one)
# db.session.add(pet_one)
# db.session.commit()

#
# user = Person.query.filter_by(id=1).first()
# print(user.name)
#
#
#
#
#

app.secret_key = 'super secret string'  # todo Change this

login_manager = flask_login.LoginManager()
login_manager.init_app(app)


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(username):
    db_user = DB_User.query.filter_by(username=username).first()
    if db_user is None:
        return
    user = User()
    user.id = username
    return user


# @login_manager.request_loader
# def request_loader(request):
#     print("call")
#     email = request.form.get('email')
#     if email not in users:
#         return
#
#     user = User()
#     user.id = email
#
#     # DO NOT ever store passwords in plaintext and always compare password
#     # hashes using constant-time comparison!
#     user.is_authenticated = request.form['pw'] == users[email]['pw']
#
#     return user

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        username = request.form['username']
        db_user = DB_User.query.filter_by(username=username).first()
        if db_user is not None:
            if request.form['password'] == db_user.password:
                user = User()
                user.id = username
                flask_login.login_user(user)
                return redirect(url_for('protected'))

    return 'Bad login'


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    if request.method == 'POST':
        username = request.form['username']
        db_user = DB_User.query.filter_by(username=username).first()
        if db_user is None:
            new_user = DB_User(username,
                               request.form['password'],
                               request.form['credit_card'],
                               request.form['address'],
                               request.form['phone'],
                               False)
            db.session.add(new_user)
            db.session.commit()

            user = User()
            user.id = username
            flask_login.login_user(user)
            return redirect(url_for('protected'))

    return 'Bad Sign Up'


@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id


@app.route('/admin')
@flask_login.login_required
def admin():
    db_user = DB_User.query.filter_by(username=flask_login.current_user.id).first()
    if db_user.admin:
        return "Welcome admin! Logged in as " + flask_login.current_user.id
    return "Access denied! Only admin can view this page"

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
