import os
from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo
from pymongo import MongoClient

app = Flask(__name__,template_folder='chairmanapp/templates')


app.secret_key = 'bfa78cc0ba1181880f980b0dd504c11c'


app.debug = True


app.config['ALLOWED_HOSTS'] = ['*']
app.config['MONGO_URI'] = 'mongodb://localhost:27017/digitalsociety'
mongo = PyMongo(app)
mongo = MongoClient(app.config['MONGO_URI'])
db = mongo.digitalsociety

# Other Flask configurations
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['STATIC_URL'] = '/static/'

# Import Flask models
from chairmanapp.models import User, Chairman
from societymemberapp.models import Societymember


# Register the blueprints 
from chairmanapp.routes import chairmanapp_bp
from societymemberapp.routes import societymemberapp_bp 

app.register_blueprint(chairmanapp_bp, url_prefix='/chairmanapp')
app.register_blueprint(societymemberapp_bp)


@app.route('/')
def home():
    return render_template('chairmanapp/index.html')

@app.route('/index/')
def index():
    
    users = user_collection.find()
    chairmen = chairman_collection.find()
    societymembers = societymember_collection.find()
    return render_template('admin.html', users=users, chairmen=chairmen, societymembers=societymembers)



@app.route('/societymember')
def societymember():
    return render_template('societymember/index.html')

@app.route('/chairmanapp/login/', methods=['GET', 'POST'])
def chairman_login():
    # Your chairman login route code here
    return render_template("chairmanapp/login.html")

@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(**data)
    mongo.db.users.insert_one(user.__dict__)
    return 'User created successfully'


if __name__ == '__main__':
    app.run(debug=True)
