from flask import Flask, url_for, request, json, jsonify
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
    password = db.Column('password', db.CHAR(20), primary_key=True)
    credit_card = db.Column('credit_card', db.CHAR(20))
    address = db.Column('address',db.CHAR(20))
    phone = db.Column('phone',db.CHAR(20))

    def __init__(self, username, password,credit_card,address,phone):
        self.username = username
        self.password = password
        self.credit_card=credit_card
        self.address = address
        self.phone = phone




# db.create_all()
# db.session.commit()
#
# some_user = DB_User('zhanghao','password','34523423432','345345kasfjsd RD','435346545')
# db.session.add(some_user)
# db.session.commit()

user1 = DB_User.query.filter_by(username='zhanghao',password='password').first()
print(user1.username)



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

users = {'test': {'pw': 'password'}}


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['pw'] == users[email]['pw']

    return user


@app.route('/')
def index():
    return redirect(url_for('login'))
    # return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'></input>
                <input type='password' name='pw' id='pw' placeholder='password'></input>
                <input type='submit' name='submit'></input>
               </form>
               '''

    email = request.form['email']
    if request.form['pw'] == users[email]['pw']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return redirect(url_for('protected'))

    return 'Bad login'


@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'


@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'


@app.route('/debug')
def debug():
    return str(users)


if __name__ == '__main__':
    app.run()
