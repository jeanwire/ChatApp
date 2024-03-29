from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

base_folder = os.path.dirname(__file__)
sk_file = os.path.join(base_folder, 'secret_key.txt')
with open(sk_file, 'r') as sk:
    app.secret_key = sk.read().strip()

CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:G8AR7Cseu5bTh9pPttcX@localhost/chatapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    messages_sent = db.relationship('Message', foreign_keys='Message.sender', backref='sender_id')
    messages_received = db.relationship('Message', foreign_keys='Message.receiver', backref='receiver_id')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    timestamp = db.Column(db.DateTime)
    sender = db.Column(db.Integer, db.ForeignKey('users.id'))
    receiver = db.Column(db.Integer, db.ForeignKey('users.id'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def test():
    return '<h1>Flask is working</h1>'

@app.route('/login', methods=['POST'])
def index():
    request_data = request.get_json()
    username = request_data[username]
    password = request_data[password]
    user_data = User.query.filter_by(username=username).first()
    authenticated = user_data.verify_password(password)
    if authenticated:
        login_user(user_data, False)
        return Response(user_data.id, status=200, mimetype='application/json')
    return Response(status=401, mimetype='application/json')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return Response(status=200, mimetype='application/json')


@app.route('/chats')
@login_required
def chats():
    return '<h1>Chats go here!</h1>'
    # username is stored in frontend, included in post requests
