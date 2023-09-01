from flask import Blueprint, render_template, request, redirect, session

from chairmanapp.models import Chairman
from societymemberapp.models import User

societymemberapp_bp = Blueprint('societymemberapp', __name__)

@societymemberapp_bp.route('/societymember_profile', methods=['GET', 'POST'])
def societymember_profile():
    from app import db
    if "email" in session:
        uid = db.users.find_one({"email": session['email']})
        sid = db.societymembers.find_one({"user_id": uid["_id"]})

        if request.method == 'POST':
            firstname = request.form['firstname']
            lastname = request.form['lastname']

            # Update the document in the MongoDB collection
            db.societymembers.update_one(
                {"_id": sid["_id"]},
                {"$set": {"firstname": firstname, "lastname": lastname}}
            )

            context = {
                'uid': uid,
                'sid': sid,
            }
            return render_template("societymemberapp/profile.html", context=context)
        else:
            context = {
                'uid': uid,
                'sid': sid,
            }
            return render_template("societymemberapp/profile.html", context=context)
    else:
        return redirect("login")

@societymemberapp_bp.route('/societymember_change_password', methods=['POST'])
def societymember_change_password():
    from app import db
    if "email" in session:
        uid = db.users.find_one({"email": session['email']})
        sid = db.societymembers.find_one({"user_id": uid["_id"]})

        if request.method == 'POST':
            currentpassword = request.form['currentpassword']
            newpassword = request.form['newpassword']

            if uid["password"] == currentpassword:
                # Update the password in the DB collection
                db.users.update_one(
                    {"_id": uid["_id"]},
                    {"$set": {"password": newpassword}}
                )
                return redirect("logout")

        context = {
            'uid': uid,
            'sid': sid,
        }
        return render_template("societymemberapp/profile.html", context=context)
