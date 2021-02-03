from flask import Flask, Blueprint, request, jsonify
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow 
from flask_migrate import Migrate
import os 
import sys
print(sys.path)

# Init app
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
basedir = os.path.abspath(os.path.dirname(__file__))


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
    name = db.Column(db.String(128))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.id) 
         
# User Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = (
            'id',
            'name'
        )

# Init Schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Create a User
@app.route('/api/user', methods=['POST'])
@cross_origin()
def add_user():
  name = request.json['name']

  new_user = User(name)

  db.session.add(new_user)
  db.session.commit()

  return user_schema.jsonify(new_user)

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