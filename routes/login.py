from flask import Blueprint, render_template, request, flash, redirect, session, url_for
from models.user import User
import duo_universal
from extensions import db

login_bp = Blueprint("login", __name__)

try:
    client_id = "DIXMG6WOX6PVM0ACQ5SK"
    client_secret="UnHVYccJdNhkHUVbBUz6kd2HcHH0n2wq9O0BHEIV"
    api_hostname="api-c31233b9.duosecurity.com"
    redirect_uri = "http://localhost:5000/duo-callback"
                
                
    duo_client = duo_universal.Client(client_id, client_secret, api_hostname, redirect_uri)
except Exception:
    pass

@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("user")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            
            
            try:
                duo_client.health_check()
            except duo_universal.DuoException:
                print("dsafdjhdfsjhkdsfahjkfdaskjhfadsjkdfs")
            # Either allow login without 2FA, or abort the login process
            
            state = duo_client.generate_state()
            session['state'] = state
            session["user"] = user.username
            
            
            prompt_uri = duo_client.create_auth_url(username, state)
            
            print("HAHHAHAHA")
            return redirect(prompt_uri)
            
            
            
            
            flash("Login successful!", "success")
            
            
            
            
            return redirect(url_for("hub.hub"))
        else:
            flash("Invalid username or password.", "error")

    
    print("Ahhhh")
    return render_template("login.html")

@login_bp.route("/logout")
def logout():
    session.pop("user", None)
    session.pop('_flashes',None)
    flash("You have been logged out.", "info")
    return redirect(url_for("login.login"))


"""
@login_bp.route("/hub", methods=["GET", "POST"])
def hub():
    if "user" in session:
        return render_template("hub.html", username=session["username"])
    else:
        return redirect(url_for("login.login"))
"""


@login_bp.route("/duo-callback")
def duo_callback():
    

    state = request.args.get('state')
    code = request.args.get('duo_code')
    
    if 'state' in session and 'user' in session:
        saved_state = session['state']
        username = session['user']
    else:
        print(session)
        # For flask, if url used to get to login.html is not localhost,
        # (ex: 127.0.0.1) then the sessions will be different
        # and the localhost session does not have the state
        print("damnit")
        return render_template("login.html",
                               message="No saved state please login again")
   
   
    if state != saved_state:
        return redirect(url_for("hub.hub"))
       #abot login
        pass
       
    try:
        username = session["user"] 
        decoded_token = duo_client.exchange_authorization_code_for_2fa_result(code, username)
    except duo_universal.DuoException as e:
        pass
    return render_template("hub.html", username=session["user"])
    return redirect(url_for("hub.hub"))
  # Handle authentication failure.
# User successfully passed Duo authentication.

