from flask import render_template, request, redirect, session, Blueprint, jsonify



from chairmanapp.models import Chairman
from societymemberapp.models import User

chairmanapp_bp = Blueprint('chairmanapp', __name__)

@chairmanapp_bp.route('/insert_sample_data', methods=['GET'])
def insert_sample_data():
    from app import db
    # Sample data to insert  the MongoDB collection
    sample_data = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'role': 'chairman'
    }

    # Insert the sample data into a MongoDB collection (e.g., 'users')
    try:
        db.users.insert_one(sample_data)
        return jsonify({'message': 'Sample data inserted successfully.'})
    except Exception as e:
        return jsonify({'error': str(e)})

@chairmanapp_bp.route('/')
def home():
    from app import db
    if "email" in session:
        uid = db.users.find_one({"email": session['email']})
        cid = db.chairman.find_one({"user_id": uid['_id']})
        if uid['role'] == "chairman" and cid:
            print("Found chairman data:", cid) 
            context = {
                'uid': uid,
                'cid': cid,
            }
            return render_template("chairmanapp/index.html", **context) # Pass context as keyword arguments
        else:
            sid = db.societymember.find_one({"user_id": uid['_id']})
            context = {
                'uid': uid,
                'sid': sid,
            }
            return render_template("societymemberapp/index.html",**context)  # Pass context as keyword arguments
    else:
        return redirect("login")

# Implement the rest of your views here in a similar way


@chairmanapp_bp.route('/login/', methods=['GET', 'POST'])
def login():
    from app import db
    if "email" in session:
        return redirect('home')
    else:
        if request.method == 'POST':
            pemail = request.form['email']
            ppassword = request.form['password']
            
            user =db.users.find_one({"email": pemail})
            
            if user and user['password'] == ppassword:
                session['email'] = user['email']
                return redirect("home")
            else:
                emsg = "Invalid email address or password"
                return render_template("chairmanapp/login.html", emsg=emsg)
        else:
            return render_template("chairmanapp/login.html")

@chairmanapp_bp.route('/logout/')
def logout():
    from app import db
    if "email" in session:
        session.pop('email', None)
    return redirect("login")

@chairmanapp_bp.route('/chairman-profile/', methods=['GET', 'POST'])
def chairman_profile():
    from app import db
    if "email" in session:
        email = session['email']
        user = db.users.find_one({"email": email})
        chairman = db.chairman.find_one({"user_id": user['_id']})

        if request.method == 'POST':
            firstname = request.form['firstname']
            lastname = request.form['lastname']

            chairman['firstname'] = firstname
            chairman['lastname'] = lastname

            db.chairman.update({"user_id": user['_id']}, chairman)
        
        context = {
            'uid': user,
            'cid': chairman,
        }
        return render_template("chairmanapp/profile.html", context=context)
    else:
        return redirect("login")

@chairmanapp_bp.route('/chairman-change-password/', methods=['GET', 'POST'])
def chairman_change_password():
    from app import db
    if "email" in session:
        email = session['email']
        user = db.users.find_one({"email": email})

        if request.method == 'POST':
            currentpassword = request.form['currentpassword']
            newpassword = request.form['newpassword']

            if user['password'] == currentpassword:
                user['password'] = newpassword
                db.users.update({"_id": user['_id']}, user)
                return redirect("logout")

        context = {
            'uid': user,
        }
        return render_template("chairmanapp/profile.html", context=context)
    else:
        return redirect("login")

#html 
@chairmanapp_bp.route('/doctor/events')
def events():
    # Your view logic here
    return render_template('chairmanapp/events.html')

@chairmanapp_bp.route('/app/inbox')
def inbox():
    # Your view logic here
    return render_template('chairmanapp/inbox.html')
