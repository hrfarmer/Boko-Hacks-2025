from flask import Blueprint, render_template, request, flash, redirect, session, url_for
from models.user import User
from extensions import db
import duo_universal
import os
import dotenv


dotenv.load_dotenv()


login_bp = Blueprint("login", __name__)


try:
    client_id = os.getenv('CLIENT_ID')
    client_secret=os.getenv('CLIENT_SECRET')
    api_hostname=os.getenv('API_HOSTNAME')
    redirect_uri = "http://localhost:5000/duo-callback"
                
                
    duo_client = duo_universal.Client(client_id, client_secret, api_hostname, redirect_uri)
except Exception:
    pass



@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            
            state = duo_client.generate_state()
            session['state'] = state
            session['user'] = user.username
            prompt_uri = duo_client.create_auth_url(username, state)

    # Redirect to prompt URI which will redirect to the client's redirect URI
    # after 2FA
            print("before")
            return redirect(prompt_uri)
            print("after")
            flash("Login successful!", "success")
            return redirect(url_for("hub.hub"))
        else:
            flash("Invalid username or password.", "error")
        
    
    print("dfdfsdfsfdsfd")
    return render_template("login.html")

@login_bp.route("/logout")
def logout():
    session.pop("user", None)
    session.pop('_flashes',None)
    flash("You have been logged out.", "info")
    return redirect(url_for("login.login"))


@login_bp.route("/duo-callback")
def duo_callback():
    # Get state to verify consistency and originality
    state = request.args.get('state')

    # Get authorization token to trade for 2FA
    code = request.args.get('duo_code')

    if 'state' in session and 'user' in session:
        print('here')
        saved_state = session['state']
        username = session['user']
        
    else:
        print('down here')
        # For flask, if url used to get to login.html is not localhost,
        # (ex: 127.0.0.1) then the sessions will be different
        # and the localhost session does not have the state
        return render_template("login.html")
                              
        
    if state != saved_state:
        return render_template("login.html")

    decoded_token = duo_client.exchange_authorization_code_for_2fa_result(code, username)
    print("ddajfj")
    return redirect(url_for("hub.hub"))
    # Exchange happened successfully so render success page
    return render_template("hub.html")