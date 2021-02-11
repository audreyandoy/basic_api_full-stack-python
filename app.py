from flask import Flask, Blueprint, Response, session, request, jsonify, redirect, url_for
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow 
from flask_migrate import Migrate
from google.oauth2 import id_token
from google.auth.transport import requests

# request = requests.Request()
CLIENT_ID = '415751135697-3pkh803j85i6gpth64lnbjc99i1bevbk.apps.googleusercontent.com'


# Init app
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///workshop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Init marshmallow ORM
ma = Marshmallow(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    first_name = db.Column(db.String(128))

    def __init__(self, email, last_name, first_name):
        self.email = email 
        self.last_name = last_name
        self.first_name = first_name 

    def __repr__(self):
        return '<id {}>'.format(self.id) 
         
# User Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = (
            'id',
            'email',
            'last_name',
            'first_name'
        )

# Init Schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Create a User
@app.route('/api/user', methods=['POST'])
@cross_origin()
def add_user():
    email = request.json['data']['email']
    last_name = request.json['data']['last_name']
    first_name = request.json['data']['first_name']

    new_user = User(email, last_name, first_name)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

requested = requests.Request()

@app.route("/login", methods = ['POST'])
@cross_origin()
def login():
    token = {'id_token': request.json['data']['id_token']}
    email = request.json['data']['email']
    last_name = request.json['data']['last_name']
    first_name = request.json['data']['first_name']
    try:
        id_info = id_token.verify_oauth2_token(token['id_token'], requested, CLIENT_ID)
        print("verified token")

        if email is None:
            return("/", {"message": "gmail could not be saved"})
        if User.query.filter_by(email = email).first() is not None:
            return({"route": "users", "data": request.json['data']['first_name']})
        else:
            add_user()
            return({"route": "users", "data": request.json['data']['first_name']})
        
    except ValueError:
        print("no token")
        content = {"message": "invalid token"}
        return Response(content, "/")
   

# Get All Users
@app.route('/api/user', methods=['GET'])
@cross_origin()
def get_users():
  all_users = User.query.all()
  result = users_schema.dump(all_users)
  return jsonify(result)

# Get Single User
@app.route('/api/user/<id>', methods=['GET'])
@cross_origin()
def get_user(id):
  user = User.query.get(id)
  return user_schema.jsonify(user)

@app.route('/api/user/<id>', methods=['DELETE'])
@cross_origin()
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)

@app.route('/')
@cross_origin()
def hello():
    return "Hello World!"


if __name__ == '__main__':
    app.run(debug=True)
