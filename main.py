# Importing necessary modules from Flask and other libraries
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_swagger_ui import get_swaggerui_blueprint  
import os

# Creating a Flask application instance
app = Flask(__name__)

# Determine the directory of the current file to help construct the database path
basedir = os.path.dirname(os.path.realpath(__file__))

# Configure the application with the URL for the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and create all tables in the database
# Initializing extensions for the Flask application
db = SQLAlchemy(app)  # Database ORM
ma = Marshmallow(app) # Serialization/Deserialization
migrate = Migrate(app, db)  # Database migration tool

# Definition of the User model class, representing a table in the database
class User(db.Model):
    UserID = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(100))
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200))
    phone_number = db.Column(db.String(20), unique=True)

    def __init__(self, UserName, email, password, phone_number):
        self.UserName = UserName
        self.email = email
        self.password = generate_password_hash(password)  # Hashing the password for security
        self.phone_number = phone_number

# Marshmallow schema for serializing and deserializing User instances
class UserSchema(ma.Schema):
    class Meta:
        fields = ('UserID', 'UserName', 'email', 'password', 'phone_number')

# Creating instances of the schema for single user and multiple users
user_schema = UserSchema()
user_schemas = UserSchema(many=True)

# Swagger configuration
SWAGGER_URL = '/swagger'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.json'  # Our API url (can of course be a local resource)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    }
)

# Register blueprint at URL
# (URL must match the one given to factory function above)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Route for the homepage
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

# Route for handling user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get data from the submitted form
        UserName = request.form['username'] 
        Email = request.form['email']
        Password = request.form['password']
        Phone_Number = request.form['phone_number']
        
        # Create a new User instance
        new_user = User(UserName, Email, Password, Phone_Number)
        # Add the new user to the database session and commit to save in the database
        db.session.add(new_user)
        db.session.commit()

        # Redirect to the login page after successful registration
        return redirect(url_for('login'))

    # If it's a GET request, display the registration form
    return render_template('register.html')

# Route for handling user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get login credentials from the form
        email = request.form['email']
        password = request.form['password']
        # Query the database for a user with the given email
        user = User.query.filter_by(email=email).first()
        # Check if the user exists and the password hash matches
        if user and check_password_hash(user.password, password):
            # If credentials are valid, redirect to the users list page
            return redirect('/user')
        else:
            # If credentials are invalid, flash an error message to be displayed
            return render_template('login.html')
    # If it's a GET request or credentials are invalid, show the login form
    return render_template('login.html')

# Route for listing all users
@app.route('/user', methods=['GET'])
def getAllUsers():
    # Query all users from the database
    all_users = User.query.all()
    # Serialize the query result to JSON-like structure
    result = user_schemas.dump(all_users)
    # Render the users template, passing the serialized users to the template
    return render_template('users.html', users=result)

# Main entry point to run the application
if __name__ == '__main__':
    app.run(debug=True, port=5000)
