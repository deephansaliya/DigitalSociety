import os
from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo
from pymongo import MongoClient

app = Flask(__name__)

# Equivalent to SECRET_KEY in Django
app.secret_key = 'bfa78cc0ba1181880f980b0dd504c11c'

# Equivalent to DEBUG in Django
app.debug = True

# Equivalent to ALLOWED_HOSTS in Django (for development)
app.config['ALLOWED_HOSTS'] = ['*']

# Equivalent to DATABASES in Django
# You'll need to configure your MongoDB connection here
# You can use libraries like Flask-PyMongo or pymongo to work with MongoDB
app.config['MONGO_URI'] = 'mongodb://localhost:27017/digitalsociety'
mongo = PyMongo(app)
mongo = MongoClient(app.config['MONGO_URI'])
db = mongo.digitalsociety# admin.py 

# Other Flask configurations
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['STATIC_URL'] = '/static/'

# Import your Flask models
from chairmanapp.models import User, Chairman
from societymemberapp.models import Societymember


# Register the blueprints for your app's parts

from chairmanapp.routes import chairmanapp_bp
from societymemberapp.routes import societymemberapp_bp # apps.py

app.register_blueprint(chairmanapp_bp)
app.register_blueprint(societymemberapp_bp)


@app.route('/')
def home():
    return render_template('chairmanapp/index.html')

@app.route('/admin/') # admin.py
def admin():
    # Implement your admin logic here
    # You can retrieve data from MongoDB collections and render templates as needed
    users = user_collection.find()
    chairmen = chairman_collection.find()
    societymembers = societymember_collection.find()
    return render_template('admin.html', users=users, chairmen=chairmen, societymembers=societymembers)



@app.route('/societymember')
def societymember():
    return render_template('societymember/index.html')

@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(**data)
    mongo.db.users.insert_one(user.__dict__)
    return 'User created successfully'


if __name__ == '__main__':
    app.run(debug=True)
