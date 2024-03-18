from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate



import os

app = Flask(__name__)

basedir = os.path.dirname(os.path.realpath(__file__))


app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Flask-Migrate

db=SQLAlchemy(app)
ma=Marshmallow(app)

class User(db.Model):
    UserID = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(100)) 
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200))
    phone_number = db.Column(db.String(20),unique=True)  

    def __init__(self, UserName, email, password, phone_number):
        self.UserName = UserName
        self.email = email
        self.password = password
        self.phone_number = phone_number
        
        
class UserSchema(ma.Schema):
    class Meta:
        fields = ('UserID', 'UserName', 'email','password','phone_number')


user_schema=UserSchema()
user_schemas=UserSchema(many=True)



@app.route('/',methods=['GET'])
def home():
    return jsonify({'msg':"welcome to mahmoud test"})

# Add a new user to the db
@app.route('/user', methods=['POST'])
def add_user():
    UserName = request.form['username']
    Email = request.form['email']
    Password = request.form['password']
    Phone_Number = request.form['phone_number']
    new_user = User(UserName, Email, Password, Phone_Number)
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user)


# Show all users
@app.route('/user',methods=['GET'])
def getAllUsers():
    all_users =User.query.all()
    result = user_schemas.dump(all_users)
    return jsonify(result)


#the regestiration form 
@app.route('/register')
def register():
    return render_template('index.html')

migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True,port=5000)
    
    
    