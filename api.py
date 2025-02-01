from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"User(name= {self.name}, email={self.email})"


user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=True, help="Name cannot be blank")
user_args.add_argument('email', type=str, required=True, help="Email cannot be blank")

UserFields = {
    "id": fields.Integer,
    "name": fields.String,
    "email": fields.String
}

class Users(Resource):
    @marshal_with(UserFields)
    def get(self):
        users = UserModel.query.all()
        return users

    @marshal_with(UserFields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(name=args["name"], email=args["email"])
        db.session.add(user)
        db.session.commit()
        return user, 201  # Return the created user

class User(Resource):
    @marshal_with(UserFields)
    def get(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message="User not found")
        return user

    @marshal_with(UserFields)
    def patch(self, id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message="User not found")
        
        user.name = args["name"]
        user.email = args["email"]
        db.session.commit()
        return user

    @marshal_with(UserFields)
    def delete(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message="User not found")
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted successfully"}, 200 #return a mesage


api.add_resource(Users, '/api/users/')
api.add_resource(User, '/api/user/<int:id>')

@app.route('/')
def home():
    return "<h1>User management REST API</h1>"


if __name__ == '__main__':
    with app.app_context():
        db.create_all() # this is to create the database if it doesn't exist yet
    app.run(debug=True)